"""Small GUI for displaying resource discovery progress to the user."""

import collections
import threading
import Tkinter as tk
import tkMessageBox
import ttk


class LifetimeError(Exception):
    """Progress was interrupted (i.e., window closed or cancel button was pressed)."""
    pass

class GuiProgressBar(ttk.Frame):
    def __init__(self, title, work_count, work_func, *func_args):
        ttk.Frame.__init__(self, relief='ridge', borderwidth=2)
        self.work_count = work_count
        self.worker_task = threading.Thread(target=work_func, args=func_args)
        self.pending_stop = False
        self.master.title(title)
        self.master.protocol('WM_DELETE_WINDOW', self._confirm_quit)
        self.pack(fill='both', expand=1)
        self.widget_space = self._create_widgets()

    def _create_widgets(self):
        # storage for widgets so we don't pollute GUI app instance namespace
        widget_space = collections.namedtuple('WidgetSpace', [
            'button_text',
            'button',
            'label_frame',
            'label_text',
            'label',
            'progress_bar',
            'status_label_text',
            'status_label'
        ])

        button_text = tk.StringVar(value='Start')
        button = ttk.Button(self, textvariable=button_text, command=self._start)
        button.pack()

        label_frame = ttk.LabelFrame(self, text='Service:Region')
        label_frame.pack(fill='x')

        label_text = tk.StringVar()
        label = ttk.Label(label_frame, anchor='w', textvariable=label_text)
        label.pack(fill='x')


        #XXX: add small fraction to max so progress bar doesn't wrap when work finishes
        progress_bar = ttk.Progressbar(
            self,
            orient='horizontal',
            length=self.master.winfo_screenwidth()/5,
            mode='determinate',
            maximum=self.work_count+1e-10
        )
        progress_bar.pack(fill='both')

        status_label_text = tk.StringVar(value='0 / {}'.format(self.work_count))
        status_label = ttk.Label(self, anchor='w', textvariable=status_label_text)
        status_label.pack(fill='x')

        return widget_space(button_text,
                            button,
                            label_frame,
                            label_text,
                            label,
                            progress_bar,
                            status_label_text,
                            status_label)

    def _confirm_quit(self):
        if tkMessageBox.askyesno(message='Quit?'):
            self.pending_stop = True
            self.master.destroy()

    def _confirm_cancel(self):
        if tkMessageBox.askyesno(message='Cancel?'):
            self.pending_stop = True
            self.widget_space.button_text.set('Canceled')
            self.widget_space.button.state(['disabled'])

    def _start(self):
        self.widget_space.button_text.set('Cancel')
        self.widget_space.button['command'] = self._confirm_cancel
        self.worker_task.start()

    def update_progress(self, delta):
        """Update progress bar.

        :param float delta: increment progress by some amount"""
        if self.pending_stop:
            raise LifetimeError('User initiated stop.')
        self.widget_space.progress_bar.step(delta)
        self.widget_space.status_label_text.set('{} / {}'.format(
            int(self.widget_space.progress_bar['value']),
            self.work_count
        ))

    def update_svc_text(self, svc_name, region):
        """Update text in status area of GUI.

        :param str svc_name: service name
        :param str region: region name
        """
        self.widget_space.label_text.set('{}:{}'.format(svc_name, region))

    def finish_work(self):
        """Update GUI when work is complete."""
        self.widget_space.button.state(['disabled'])
        self.widget_space.button_text.set('Finished')
