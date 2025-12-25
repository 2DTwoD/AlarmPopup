from tkinter import Image, Toplevel, Menu
from tkinter import Tk
from rx.subjects import Subject

import keyboard

from pystray import MenuItem as item
import pystray

from PIL import Image


class MainWindow(Tk):
    def __init__(self, title="App", size='100x100', show_tag_viewer_subject: Subject=None):
        super().__init__()
        self.geometry(size)
        self.resizable(False, False)
        self.title(title)

        self.icon = None
        keyboard.add_hotkey('F4', self._hotKet)

        self.protocol('WM_DELETE_WINDOW', self.hideWindow)

        self.attributes('-toolwindow', True)
        self.attributes("-topmost", True)
        self.resizable(False, False)

        image = Image.open("ico.png")
        icon_menu = (item('Показать (F4)', self.showWindow, default=True), pystray.Menu.SEPARATOR, item('Выход', self.quitWindow))
        self.icon = pystray.Icon("name", image, "title", icon_menu)
        self.icon.run_detached()

        window_menu = Menu(self)

        action = Menu(window_menu, tearoff=0)
        window_menu.add_cascade(label='Действие', menu=action)
        action.add_command(label='Скрыть (F4)', command=lambda: self.hideWindow())
        action.add_separator()
        action.add_command(label='Выключить', command=lambda: self.quitWindow())
        show_tag_viewer = Menu(window_menu, tearoff=0)
        window_menu.add_cascade(label='OPC', menu=show_tag_viewer)
        show_tag_viewer.add_command(label='Тэги', command=lambda: show_tag_viewer_subject.on_next(True))

        self.config(menu=window_menu)
        # self.hideWindow()

    def showWindow(self):
        self.after(0, self.deiconify)

    def hideWindow(self):
        self.withdraw()

    def quitWindow(self):
        self.icon.visible = False
        self.icon.stop()
        self.destroy()

    def _hotKet(self):
        if self.winfo_viewable():
            self.hideWindow()
        else:
            self.showWindow()
