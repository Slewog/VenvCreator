import sys

# from PIL.ImageFile import ImageFile
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
    def __init__(self, master: CTk, current_path: str, font: CTkFont):
        super().__init__(master, fg_color=const.FRAME_COLORS)

        img = pillow_open_img(os_path_join(current_path, "assets", 'python.png'))

        self.head_logo = CTkLabel(
            self,
            image=CTkImage(light_image=img, dark_image=img, size=(150, 150)),
            text=""
        )
        self.head_logo.grid(column=0, row=0)
        del img

        self.head_label = CTkLabel(
            self,
            text='Create a Python virtual environment:',
            font=font
        )
        self.head_label.grid(column=0, row=1, pady=(5, 0))


class NameFrame(CTkFrame):
    def __init__(self, master: CTkFrame, bold12: CTkFont):
        super().__init__(master, fg_color=const.FRAME_COLORS)

        env_name_label = CTkLabel(
            self,
            text='Environment name:',
            font=bold12
        )
        env_name_label.grid(column=0, row=0)

        self.env_name_entry = CTkEntry(
            self,
            width=const.ENTRY_WIDTH,
            placeholder_text='Name of your venv',
            font=bold12
        )
        self.env_name_entry.grid(column=1, row=0, padx=(20, 0))


class DirFrame(CTkFrame):
    def __init__(self, master: CTkFrame, bold12: CTkFont, bold15: CTkFont):
        super().__init__(master, fg_color=const.FRAME_COLORS)

        env_path_label = CTkLabel(
            self,
            text='Project Directory:',
            font=bold12
        )
        env_path_label.grid(column=0, row=0)

        self.env_path_entry = CTkEntry(
            self,
            width=const.ENTRY_WIDTH,
            state='disabled',
            font=bold12
        )
        self.env_path_entry.grid(column=1, row=0, padx=(20, 20))

        btn_browse = CTkButton(
            self,
            text="BROWSE",
            width=85,
            font=bold15
        )
        btn_browse.grid(column=2, row=0)


class MainFrame(CTkFrame):
    def __init__(self, master: CTk, bold12: CTkFont, bold15: CTkFont):
        super().__init__(master, fg_color=const.FRAME_COLORS)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.name_frame = NameFrame(self, bold12)
        self.name_frame.grid(column=0, row=0, pady=(15, 30))

        self.dir_frame = DirFrame(self, bold12, bold15)
        self.dir_frame.grid(column=0, row=1, pady=(0, 30))

        self.btn_send = CTkButton(
            self,
            text="Create your Virtual Env",
            font=bold15,
        )
        self.btn_send.grid(column=0, row=2)


class App(CTk):
    def __init__(self):
        super().__init__()
        self.bind('<Escape>', lambda e: self.destroy()) # Bind Escape key to close the app.

        # Get absolute path, works for dev and for PyInstaller.
        self.current_path = getattr(sys, '_MEIPASS', os_path_dirname(os_path_abspath(__file__)))

        bold12 = CTkFont(family=const.FONT_FAMILY, size=12, weight="bold")
        bold15 = CTkFont(family=const.FONT_FAMILY, size=15, weight="bold")

        self.title(const.SCREEN_TITLE)
        self.resizable(width=const.SCREEN_RESIZABLE, height=const.SCREEN_RESIZABLE)
        self.iconbitmap(os_path_join(self.current_path, "assets", const.SCREEN_ICON))
        self.geometry(self.get_display_center(const.SCREEN_W, const.SCREEN_H))

        self.grid_columnconfigure(0, weight=1)

        self.head_frame = HeaderFrame(self, self.current_path, bold15)
        self.head_frame.grid(column=0, row=0, pady=(15, 20))

        self.main_frame = MainFrame(self, bold12, bold15)
        self.main_frame.grid(column=0, row=1, sticky='ew', padx=10)

        copyright = CTkLabel(
            self,
            text='Slewog Software @ All Rights Reserved',
            font=(const.FONT_FAMILY, 12, 'bold', 'roman', 'underline')
        )
        copyright.grid(column=0, row=3, pady=(30, 0))

        self.update()

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