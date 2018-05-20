"""
Ignore certain operations. There are a few reasons to ignore them. Some don't actually apply to
account resources. Others may be too verbose or not relevant for some users of this tool.
"""

import ConfigParser
import logging


LOGGER = logging.getLogger(__name__)

class BlacklistError(Exception):
    """Generic error for parsing the operations blacklist."""
    pass

class OpBlacklistParser(object):
    """Parser for operations blacklist."""

    def __init__(self, blacklist_fp, api_model):
        self.blacklist_fp = blacklist_fp
        self.api_model = api_model
        self._cfg_parser = ConfigParser.RawConfigParser(allow_no_value=True)
        self._cfg_parser.optionxform = str  # case sensitive
        self._cfg_parser.readfp(self.blacklist_fp)

        # validate blacklist configuration #

        err = False
        for svc_name in self._cfg_parser.sections():
            try:
                available_ops = set(api_model[svc_name]['ops'])
                blacklist_ops = set(self._cfg_parser.options(svc_name))
                invalid_ops = blacklist_ops - available_ops
                if invalid_ops:
                    err = True
                    LOGGER.error('[%s] Invalid operation(s): %s.', svc_name, ', '.join(invalid_ops))
            except KeyError:
                LOGGER.warning('Invalid service name "%s".', svc_name)
        if err:
            raise BlacklistError('Failure to validate blacklist file.')

    def is_blacklisted(self, svc_name, op_name):
        """
        :param str svc_name: service name
        :param str op_name: operation name
        :rtype: bool
        :return: whether operation (in a service) has been blacklisted
        """
        return self._cfg_parser.has_option(svc_name, op_name)
