from tkinter import Image
from tkinter import Tk

import keyboard

from pystray import MenuItem as item
import pystray

from PIL import Image


class MainWindow:
    def __init__(self, title="App", size='100x100'):
        self.window = Tk()
        self.window.geometry(size)
        self.window.resizable(False, False)
        self.window.title(title)

        self.icon = None
        keyboard.add_hotkey('F4', self.showWindow)

        self.window.protocol('WM_DELETE_WINDOW', self.hideWindow)

        self.window.attributes('-toolwindow', True)
        self.window.attributes("-topmost", True)
        self.window.resizable(False, False)

        image = Image.open("ico.png")
        menu = (item('Показать', self.showWindow, default=True), item('Выход', self.quitWindow))
        self.icon = pystray.Icon("name", image, "title", menu)
        self.icon.run_detached()

        # self.hideWindow()

        self.window.mainloop()

    def showWindow(self):
        self.window.after(0, self.window.deiconify)

    def hideWindow(self):
        self.window.withdraw()

    def quitWindow(self):
        self.icon.visible = False
        self.icon.stop()
        self.window.destroy()
