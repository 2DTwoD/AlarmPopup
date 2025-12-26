from datetime import datetime
from tkinter import ttk, BOTH, END, NO, RIGHT, LEFT, Y

from rx.subjects import Subject
from dateutil import parser


class MessageTable(ttk.Treeview):
    def __init__(self, master, incomming_tags_subject: Subject, show_hide_window_subject: Subject):
        super().__init__(master=master, columns=["dt", "message"], show="headings", selectmode="browse")
        self.incomming_tags_subject = incomming_tags_subject
        self.incomming_tags_subject.subscribe(lambda tags: self._newTags(tags))
        self.strokes = []
        self.show_hide_window_subject = show_hide_window_subject
        self.time_format = '%d.%m.%Y, %H:%M:%S'

        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
        style.configure('Treeview', font=('Arial', 10, 'bold'))

        self.tag_configure('stroke_style', background='red', foreground='white')

        self.heading("dt", text="Дата и время")
        self.heading("message", text="Сообщение")

        self.column("#1", stretch=NO, width=150)

        scroll = ttk.Scrollbar(master, orient="vertical", command=self.yview)
        self.configure(yscrollcommand=scroll.set)

        self.pack(fill=BOTH, side=LEFT, expand=True)
        scroll.pack(fill=Y, side=RIGHT)

    def _newTags(self, tags):
        if tags == 'OPC error':
            self.delete(*self.get_children())
            self.insert("",
                        END,
                        values=(datetime.now().strftime(self.time_format), 'Нет связи с OPC сервером'),
                        tags=['stroke_style'])
            return
        elif tags == 'clear':
            self.delete(*self.get_children())
            self.strokes = []
            return

        show = False
        strokes_change_aux = False

        for tag in tags:
            new_added, strokes_change = self._checkAndAddTag(tag)
            show = show or new_added
            strokes_change_aux = strokes_change_aux or strokes_change

        if show:
            self.show_hide_window_subject.on_next(True)

        if strokes_change_aux:
            self.delete(*self.get_children())
            for stroke in self.strokes:
                self.insert("",
                            END,
                            values=(parser.parse(stroke[3]).strftime(self.time_format), stroke[4]),
                            tags=['stroke_style'])
            if len(self.strokes) == 0:
                self.show_hide_window_subject.on_next(False)

        # print(tags)
        # print(self.strokes)
        # print('-' * 50)

    def _checkAndAddTag(self, tag):
        new_added = False
        strokes_change = False
        match = False

        if len(tag) != 5:
            print('Wrong signal, wrong len(tuple)')
            return new_added, strokes_change

        tag_name, value, status = tag[:3]
        if status != 'Good' or type(value) != bool:
            print('Wrong signal, {0} BAD or not bool'.format(tag_name))
            return new_added, strokes_change

        for stroke in self.strokes[:]:
            if stroke[0] == tag_name:
                match = True
                if not value:
                    self.strokes.remove(stroke)
                    strokes_change = True
                break

        if value and not match:
            self.strokes.append(tag)
            strokes_change = True
            new_added = True

        return new_added, strokes_change
