import sys
from os import path
import customtkinter as ctk

import const


class App(ctk.CTk):
    def __init__(self, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.bind('<Escape>', lambda e: self.destroy()) # Bind Escape key to close the app.

        # Get absolute path, works for dev and for PyInstaller.
        self.current_path = getattr(sys, '_MEIPASS', path.dirname(path.abspath(__file__)))

        self.title(const.SCREEN_TITLE)
        self.resizable(width=const.SCREEN_RESIZABLE, height=const.SCREEN_RESIZABLE)
        self.iconbitmap(path.join(self.current_path, "assets", const.SCREEN_ICON))
        self.geometry(self.get_display_center(const.SCREEN_W, const.SCREEN_H))
        self.update() # Just to get the correct values from winfo_width() and winfo_height().

    def get_display_center(self, width: int, height: int) -> str:
        """Centers the CTK window to the main display/monitor

        :returns: app geometry and position on display
        """
        s_width = self.winfo_screenwidth()
        s_height = self.winfo_screenheight()
        x = (s_width - width) // 2
        y = (s_height - height) // 2
        return f"{width}x{height}+{x}+{y}"

if __name__ == '__main__':
    app = App()
    app.mainloop()
    sys.exit()