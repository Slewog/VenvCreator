import sys
from os import path
from PIL import Image

import const
import customtkinter as ctk

ctk.set_appearance_mode('dark')


class HeaderFrame(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk, current_path: str):
        super().__init__(master)

        tmp_img = Image.open(path.join(current_path, "assets", const.HEADER['img_path']))

        head_logo = ctk.CTkLabel(
            self,
            image=ctk.CTkImage(
                light_image=tmp_img,
                dark_image=tmp_img,
                size=const.HEADER['img_size']
            ),
            text="" # Stay empty.
        )
        head_logo.grid(column=0, row=0)

        head_label = ctk.CTkLabel(
            self,
            text=const.HEADER['text'],
            font=(const.FONTS['family'], const.FONTS['size'], const.FONTS['weight'], const.FONTS['slant'])
        )
        head_label.grid(column=0, row=1, pady=const.HEADER['text_pady'])

        self.grid(column=0, row=0, pady=const.HEADER['pady'])


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.bind('<Escape>', lambda e: self.destroy()) # Bind Escape key to close the app.

        # Get absolute path, works for dev and for PyInstaller.
        self.current_path = getattr(sys, '_MEIPASS', path.dirname(path.abspath(__file__)))

        self.title(const.SCREEN_TITLE)
        self.resizable(width=const.SCREEN_RESIZABLE, height=const.SCREEN_RESIZABLE)
        self.iconbitmap(path.join(self.current_path, "assets", const.SCREEN_ICON))
        self.geometry(self.get_display_center(const.SCREEN_W, const.SCREEN_H))

        self.grid_columnconfigure(0, weight=1)

        self.head_frame = HeaderFrame(master=self, current_path=self.current_path)

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