import sys
from os import path

import const
import customtkinter as ctk


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

    def get_display_center(self, win_width: int, win_height: int) -> str:
        """Centers the CTK window to the main display.

        Args:
            win_width = Width of the app window.
            win_height = Height of the app window.

        Returns:
            Window geometry.
        """
        x = (self.winfo_screenwidth() - win_width) // 2
        y = (self.winfo_screenheight() - win_height) // 2
        return f"{win_width}x{win_height}+{x}+{y}"

if __name__ == '__main__':
    app = App()
    app.mainloop()
    sys.exit()