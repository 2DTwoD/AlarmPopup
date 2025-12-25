from tkinter import ttk, BOTH, END, NO, RIGHT, LEFT, Y

from rx.subjects import Subject
from dateutil import parser


class MessageTable(ttk.Treeview):
    def __init__(self, master, incomming_tags_subject: Subject):
        super().__init__(master=master, columns=["dt", "message"], show="headings", selectmode="browse")
        self.incomming_tags_subject = incomming_tags_subject
        self.incomming_tags_subject.subscribe(lambda tags: self._newTags(tags))
        self.strokes = []

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
        for tag in tags:
            self._checkAndAddTag(tag)
        print(tags)
        print(self.strokes)
        print('-' * 50)

    def _checkAndAddTag(self, tag):
        if len(tag) != 5:
            print('Wrong signal, wrong len(tuple)')
            return False
        tag_name, value, status = tag[:3]
        if status != 'Good' and type(value) != bool:
            print('Wrong signal, BAD or not bool')
            return False

        match = False
        change = False
        for stroke in self.strokes[:]:
            if stroke[0] == tag_name:
                match = True
                if not value:
                    self.strokes.remove(stroke)
                    change = True
                break

        if value and not match:
            self.strokes.append(tag)
            change = True

        if change:
            self.delete(*self.get_children())
            for stroke in self.strokes:
                self.insert("",
                            END,
                            values=(parser.parse(stroke[3]).strftime("%d.%m.%Y, %H:%M:%S"), stroke[4]),
                            tags=['stroke_style'])
        return True
