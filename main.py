import sys

from PIL.ImageFile import ImageFile
from PIL.Image import open as pillow_open_img

from ctypes import windll, byref
from ctypes.wintypes import RECT as ct_Rect

from os import chdir as os_goto_dir
from os.path import (
    dirname    as os_path_dirname,
    abspath    as os_path_abspath,
    join       as os_path_join,
    isdir      as os_path_isdir
)

from customtkinter import (
    set_appearance_mode as ctk_set_appearance,
    CTk,
    CTkFont,
    CTkFrame,
    CTkLabel,
    CTkEntry,
    CTkImage,
    CTkButton,
    filedialog as ctk_file_dialog
)

import const

ctk_set_appearance(const.APPEARANCE_MODE)


class HeaderFrame(CTkFrame):
    def __init__(self, master: CTk, logo: ImageFile):
        super().__init__(master)

        self.head_logo = CTkLabel(
            self,
            image=CTkImage(light_image=logo, dark_image=logo, size=const.HEADER['img_size']),
            text=""
        )
        self.head_logo.grid(column=0, row=0)

        self.head_label = CTkLabel(
            self,
            text=const.HEADER['text'],
            font=(const.FONTS['family'], const.FONTS['size'], const.FONTS['weight'], const.FONTS['slant'])
        )
        self.head_label.grid(column=0, row=1, pady=const.HEADER['text_pady'])


class App(CTk):
    def __init__(self):
        super().__init__()
        self.bind('<Escape>', lambda e: self.destroy()) # Bind Escape key to close the app.

        # Get absolute path, works for dev and for PyInstaller.
        self.current_path = getattr(sys, '_MEIPASS', os_path_dirname(os_path_abspath(__file__)))

        self.title(const.SCREEN_TITLE)
        self.resizable(width=const.SCREEN_RESIZABLE, height=const.SCREEN_RESIZABLE)
        self.iconbitmap(os_path_join(self.current_path, "assets", const.SCREEN_ICON))
        self.geometry(self.get_display_center(const.SCREEN_W, const.SCREEN_H))

        self.grid_columnconfigure(0, weight=1)

        self.head_frame = HeaderFrame(
            self,
            pillow_open_img(os_path_join(self.current_path, "assets", const.HEADER['img_path']))
        )
        self.head_frame.grid(column=0, row=0, pady=const.HEADER['pady'])

        

        self.update() # Just to get the correct values from winfo_width() and winfo_height().

    def get_display_center(self, app_width: int, app_height: int) -> str:
        """Centers the CTK window to the main display.
        Get work screen area from ctypes.

        Args:
            app_width = Width of the app window.
            app_height = Height of the app window.

        Returns:
            App geometry.
        """
        work_area = ct_Rect()
        _ = windll.user32.SystemParametersInfoW(0x0030, 0, byref(work_area), 0)
        x = (work_area.right - app_width) // 2
        y = (work_area.bottom - app_height) // 2
        return f"{app_width}x{app_height}+{x}+{y}"


if __name__ == '__main__':
    app = App()
    app.mainloop()
    sys.exit()