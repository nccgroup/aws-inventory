"""Abstraction for invoking AWS APIs (a.k.a. operations) and handling responses."""

import logging
from Queue import Queue
from threading import Thread

import botocore
from opinel.utils.credentials import read_creds

import config
import progress
import store


LOGGER = logging.getLogger(__name__)

class ApiInvoker(object):
    """Invoke APIs from GUI."""

    def __init__(self, script_args, svc_descriptors, ops_count):
        self.script_args = script_args
        self.svc_descriptors = svc_descriptors
        self.ops_count = ops_count
        self.progress_bar = None
        self.store = store.ResultStore(script_args.profile)

        # search for AWS credentials
        # using opinel allows us to use MFA and a CSV file. Otherwise, we could just use
        # botocore.session.get_session({'profile': args.profile, 'region': args.regions[0]})
        self.credentials = read_creds(
            script_args.profile,
            script_args.csv_credentials,
            script_args.mfa_serial,
            script_args.mfa_code)
        if not self.credentials['AccessKeyId']:
            raise EnvironmentError('Failed to get AWS account credentials.')
        LOGGER.info('Using AWS credential key ID: %s.', self.credentials['AccessKeyId'])

    def start(self):
        """Start the invoker with associated GUI. Wait for GUI to stop."""
        self.progress_bar = progress.GuiProgressBar(
            'AWS Inventory',
            self.ops_count,
            self._probe_services)
        self.progress_bar.mainloop()

    def _probe_services(self):
        try:
            # create a config for all clients to share
            client_config = botocore.config.Config(
                connect_timeout=config.CLIENT_CONNECT_TIMEOUT,
                read_timeout=config.CLIENT_READ_TIMEOUT
            )

            session = botocore.session.get_session()
            for svc_name in self.svc_descriptors:
                operations = self.svc_descriptors[svc_name]['ops']
                regions = self.svc_descriptors[svc_name]['regions']

                # call each API across each region
                api_version = session.get_config_variable('api_versions').get(svc_name, None)
                params = {'svc_name': svc_name,
                          'dry_run': self.script_args.dry_run,
                          'store': self.store}
                for region in regions:
                    self.progress_bar.update_svc_text(svc_name, region)
                    try:
                        client = session.create_client(
                            svc_name,
                            region_name=region,
                            api_version=api_version,
                            aws_access_key_id=self.credentials['AccessKeyId'],
                            aws_secret_access_key=self.credentials['SecretAccessKey'],
                            aws_session_token=self.credentials['SessionToken'],
                            config=client_config
                        )
                    except botocore.exceptions.NoRegionError:
                        LOGGER.warning('[%s][%s] Issue in region detection. Using default region.',
                                       config.DEFAULT_REGION,
                                       svc_name)
                        client = session.create_client(
                            svc_name,
                            region_name=config.DEFAULT_REGION,
                            api_version=api_version,
                            aws_access_key_id=self.credentials['AccessKeyId'],
                            aws_secret_access_key=self.credentials['SecretAccessKey'],
                            aws_session_token=self.credentials['SessionToken'],
                            config=client_config
                        )
                    params.update({'region': region, 'client': client})
                    # schedule worker threads to invoke all APIs. Wait until all APIs have been
                    # invoked.
                    thread_work(
                        operations,
                        self.svc_worker,
                        params)
                    self.progress_bar.update_progress(len(operations))
            self.progress_bar.finish_work()
            self.write_results()
        except progress.LifetimeError as e:
            LOGGER.debug(e)

    def write_results(self, response_dump_fp=None, exception_dump_fp=None, gui_data_fp=None):
        """Output the results, if not a dry run.

        :param file response_dump_fp: file for responses
        :param file exception_dump_fp: file for exceptions
        :param file gui_data_fp: file for GUI data
        """
        if not self.script_args.dry_run:
            if response_dump_fp:
                self.store.dump_response_store(response_dump_fp)
            elif self.script_args.responses_dump:
                with open(self.script_args.responses_dump, 'wb') as out_fp:
                    self.store.dump_response_store(out_fp)

            if exception_dump_fp:
                self.store.dump_exception_store(exception_dump_fp)
            elif self.script_args.exceptions_dump:
                with open(self.script_args.exceptions_dump, 'wb') as out_fp:
                    self.store.dump_exception_store(out_fp)

            if self.script_args.verbose:
                print self.store.get_response_store()

            if gui_data_fp:
                self.store.generate_data_file(gui_data_fp)
            else:
                with open(self.script_args.gui_data_file, 'w') as out_fp:
                    self.store.generate_data_file(out_fp)

    @staticmethod
    def svc_worker(que, params):
        """Worker thread for a service in a region.

        :param Queue que: APIs to invoke
        :param dict params: parameters to use for invoking API
        """
        svc_name = params['svc_name']
        region = params['region']
        storage = params['store']
        while True:
            try:
                svc_op = que.get()
                if svc_op is None:
                    break
                if storage.has_exceptions(svc_name, svc_op):
                    continue

                # this is the way botocore does it. See botocore/__init__.py
                py_op = botocore.xform_name(svc_op)
                LOGGER.debug('[%s][%s] Invoking API "%s". Python name "%s".',
                             region,
                             svc_name,
                             svc_op,
                             py_op)

                if not params['dry_run']:
                    if params['client'].can_paginate(py_op):
                        paginator = params['client'].get_paginator(py_op)
                        response = paginator.paginate().build_full_result()
                    else:
                        response = getattr(params['client'], py_op)()
                    storage.add_response(svc_name, region, svc_op, response)
            except Exception as e:
                storage.add_exception(svc_name, region, svc_op, e)
                LOGGER.exception(
                    'Unknown error while invoking API for service "%s" in region "%s".',
                    svc_name,
                    region)
            finally:
                que.task_done()

#XXX: borrowed from opinel because their threading module is failing to load. Pretty much the example in the Queue docs
def thread_work(targets, function, params=None):
    """Thread worker creator.

    :param list targets: changing parameters
    :param function function: callback function
    :param dict params: static parameters
    """
    que = Queue(maxsize=0)
    thread_count = min(config.MAX_THREADS, len(targets))
    if thread_count > 0:
        for _ in range(thread_count):
            worker = Thread(target=function, args=(que, params))
            worker.setDaemon(True)
            worker.start()
        for target in targets:
            que.put(target)

        # signal to threads so they know to stop
        # see issue #2
        for _ in range(thread_count):
            que.put(None)

        que.join()
    else:
        LOGGER.warning('No work to be done.')