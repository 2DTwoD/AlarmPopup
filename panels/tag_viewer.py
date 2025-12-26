from datetime import datetime
from tkinter import Toplevel, Text, ttk, LEFT, RIGHT, Y, BOTH, END
from rx.subjects import Subject


class TagViewer(Toplevel):
    def __init__(self, title="App", win_width=100, win_height=100, password='1234567890',
                 incomming_tags_subject: Subject=None,
                 show_tag_viewer_subject: Subject=None):
        super().__init__()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws / 2) - (win_width / 2)
        y = (hs / 2) - (win_height / 2)
        self.geometry('{0}x{1}+{2}+{3}'.format(win_width, win_height, int(x), int(y)))
        self.resizable(False, False)
        self.title(title)
        self.attributes('-toolwindow', True)
        self.attributes("-topmost", True)
        self.resizable(False, False)
        self.protocol('WM_DELETE_WINDOW', self.hideWindow)

        self.password = password

        incomming_tags_subject.subscribe(lambda tags: self._newTags(tags))
        show_tag_viewer_subject.subscribe(lambda password: self._check_pass_and_show(password))

        self.textArea = Text(master=self, state="disabled")
        scroll = ttk.Scrollbar(master=self, orient="vertical", command=self.textArea.yview)

        self.textArea.pack(side=LEFT, fill=BOTH, expand=True)
        scroll.pack(side=RIGHT, fill=Y)
        self.hideWindow()

    def _newTags(self, tags):
        if not self.winfo_viewable():
            return

        self.textArea.configure(state='normal')
        self.textArea.delete('1.0', END)
        if tags == 'OPC error':
            self.textArea.insert(END, '{0} OPC error'.format(datetime.now().strftime('%d.%m.%Y %H:%M:%S')))
            self.textArea.yview(END)
            return
        elif tags == 'clear':
            return
        else:
            for tag in tags:
                self.textArea.insert(END, self._get_string_from_tag(tag))
                self.textArea.yview(END)
        self.textArea.configure(state='disabled')

    def _get_string_from_tag(self, tag):
        return '{0} | {1} | {2} | {3} | {4}\n'.format(tag[3], tag[2], tag[0], tag[1], tag[4])

    def _check_pass_and_show(self, password):
        if password == self.password:
            self.showWindow()

    def showWindow(self):
        self.after(0, self.deiconify)

    def hideWindow(self):
        self.withdraw()
