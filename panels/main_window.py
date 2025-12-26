from tkinter import Menu
from tkinter import Tk
from tkinter.messagebox import askyesno
from tkinter.simpledialog import askstring

from rx.subjects import Subject

import keyboard

# from pystray import MenuItem as item
# import pystray
#
# from PIL import Image
# import threading


class MainWindow(Tk):
    def __init__(self, show_tag_viewer_subject: Subject,
                 show_hide_window_subject: Subject,
                 title="App", win_width=100, win_height=100, hotkey='F4'):
        super().__init__()
        self.hideWindow()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws / 2) - (win_width / 2)
        y = (hs / 2) - (win_height / 2)
        self.geometry('{0}x{1}+{2}+{3}'.format(win_width, win_height, int(x), int(y)))
        self.resizable(False, False)
        self.title(title)
        self.iconbitmap('icon.ico')
        self.protocol('WM_DELETE_WINDOW', self.hideWindow)
        self.attributes("-topmost", True)
        # self.attributes('-toolwindow', True)
        self.resizable(False, False)


        self.ttl = title
        self.show_tag_viewer_subject = show_tag_viewer_subject
        show_hide_window_subject.subscribe(lambda value: self.showWindowWithValue(value))

        # Hot key
        self.icon = None
        keyboard.add_hotkey(hotkey, self._hotKet)

        # Tray, not working in WinXP

        # image = Image.open("ico.png")
        # icon_menu = (item('Показать (F4)', lambda x: self.showWindow(), default=True),
        #              pystray.Menu.SEPARATOR,
        #              item('Выход', lambda x: self.quitWindow()))
        # self.icon = pystray.Icon("name", image, "title", icon_menu)
        # threading.Thread(target=lambda: self.icon.run(), daemon=True).start()

        #Menu
        window_menu = Menu(self)
        action = Menu(window_menu, tearoff=0)
        window_menu.add_cascade(label='Действие', menu=action)
        action.add_command(label='Скрыть ({0})'.format(hotkey), command=lambda: self.hideWindow())
        action.add_separator()
        action.add_command(label='Выключить', command=lambda: self.quitWindow())
        show_tag_viewer = Menu(window_menu, tearoff=0)
        window_menu.add_cascade(label='OPC', menu=show_tag_viewer)
        show_tag_viewer.add_command(label='Тэги', command=self._open_tag_viewer)
        self.config(menu=window_menu)

    def showWindowWithValue(self, value):
        if value:
            self.showWindow()
        else:
            self.hideWindow()

    def showWindow(self):
        self.after(0, self.deiconify)

    def hideWindow(self):
        # self.withdraw()
        self.iconify()

    def quitWindow(self):
        # self.icon.visible = False
        # self.icon.stop()
        if askyesno(title="Подтверждение", message="Выключить приложение {0}?".format(self.ttl)):
            self.destroy()

    def _open_tag_viewer(self):
        self.show_tag_viewer_subject.on_next(askstring("Вопрос", "Введите пароль", show='*'))

    def _hotKet(self):
        if self.winfo_viewable():
            self.hideWindow()
        else:
            self.showWindow()
