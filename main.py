import sys
import const

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

ctk_set_appearance(const.APPEARANCE_MODE)


class HeaderFrame(CTkFrame):
    def __init__(self, master: CTk, current_path: str, font: CTkFont):
        super().__init__(master, fg_color=const.FRAME_COLORS)

        img = pillow_open_img(os_path_join(current_path, "assets", 'python.png'))

        head_logo = CTkLabel(
            self,
            image=CTkImage(light_image=img, dark_image=img, size=(150, 150)),
            text=""
        )
        head_logo.grid(column=0, row=0)
        del img # Just to release memory.

        head_label = CTkLabel(self, text='Create a Python virtual environment:', font=font)
        head_label.grid(column=0, row=1, pady=(5, 0))


class MainFrame(CTkFrame):
    def __init__(self, master: CTk, bold12: CTkFont, bold15: CTkFont):
        super().__init__(master, fg_color= const.FRAME_COLORS)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        frame1 = CTkFrame(self, fg_color=const.FRAME_COLORS)
        frame1.grid(column=0, row=0, pady=(15, 30))

        env_name_label = CTkLabel(frame1, text='Environment name:', font=bold12)
        env_name_label.grid(column=0, row=0)

        self.env_name_entry = CTkEntry(frame1, width=const.ENTRY_WIDTH, placeholder_text='Name of your venv', font=bold12)
        self.env_name_entry.grid(column=1, row=0, padx=(20, 0))

        frame2 = CTkFrame(self, fg_color=const.FRAME_COLORS)
        frame2.grid(column=0, row=1, pady=(0, 40))

        env_path_label = CTkLabel(frame2, text='Project Path:', font=bold12)
        env_path_label.grid(column=0, row=0)

        self.env_path_entry = CTkEntry(frame2, width=const.ENTRY_WIDTH, state='disabled', font=bold12)
        self.env_path_entry.grid(column=1, row=0, padx=(20, 20))

        self.browse_btn = CTkButton(frame2, text="BROWSE", width=85, font=bold15)
        self.browse_btn.grid(column=2, row=0)

        self.create_btn = CTkButton(self, text="Create your Virtual Env", font=bold15)
        self.create_btn.grid(column=0, row=2, pady=(0, 1))


class App():
    def __init__(self, window: CTk):
        # Get absolute path, works for dev and for PyInstaller.
        self.current_path = getattr(sys, '_MEIPASS', os_path_dirname(os_path_abspath(__file__)))

        bold12 = CTkFont(family=const.FONT_FAMILY, size=12, weight="bold")
        bold15 = CTkFont(family=const.FONT_FAMILY, size=15, weight="bold")

        # Bind Escape key to close the app.
        window.bind('<Escape>', lambda e: window.destroy())

        window.title(const.SCREEN_TITLE)
        window.resizable(width=const.SCREEN_RESIZABLE, height=const.SCREEN_RESIZABLE)
        window.iconbitmap(os_path_join(self.current_path, "assets", const.SCREEN_ICON))
        window.geometry(self.get_display_center(const.SCREEN_W, const.SCREEN_H))
        window.grid_columnconfigure(0, weight=1)

        self.header = HeaderFrame(window, self.current_path, bold15)
        self.header.grid(column=0, row=0, pady=(15, 20))

        self.main = MainFrame(window, bold12, bold15)
        self.main.grid(column=0, row=1, sticky='ew', padx=10)

        copyright = CTkLabel(
            window,
            text='Slewog Software @ All Rights Reserved',
            font=(const.FONT_FAMILY, 12, 'bold', 'roman', 'underline')
        )
        copyright.grid(column=0, row=3, pady=(30, 0))

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
    window = CTk()
    app = App(window)
    window.update()
    window.mainloop()
    sys.exit()