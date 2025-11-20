import sys
import const
from threading import Thread
from time import sleep as t_sleep
from subprocess import run as sb_run
from PIL.Image import open as pillow_open_img

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
    CTkToplevel,
    CTkProgressBar,
    filedialog as ctk_file_dialog
)
from CTkMessagebox import CTkMessagebox

ctk_set_appearance(const.APPEARANCE_MODE)

# Get absolute path, works for dev and for PyInstaller.
DIR_PATH = getattr(sys, '_MEIPASS', os_path_dirname(os_path_abspath(__file__)))
ASSETS_PATH = os_path_join(DIR_PATH, 'assets')


def get_display_work_area():
    from ctypes import windll, byref
    from ctypes.wintypes import RECT as ct_Rect
    work_area = ct_Rect()
    _ = windll.user32.SystemParametersInfoW(0x0030, 0, byref(work_area), 0)
    del windll, byref, ct_Rect

    return {'width': work_area.right, 'height': work_area.bottom}


class HeaderFrame(CTkFrame):
    LABEL_TEXT = 'Create a Python virtual environment:'

    def __init__(self, master: CTk):
        super().__init__(master, fg_color=const.COLOR_TRANSPARENT)

        img = pillow_open_img(os_path_join(ASSETS_PATH, const.HEADER_LOGO))

        head_logo = CTkLabel(
            self,
            image=CTkImage(light_image=img, dark_image=img, size=const.HEADER_LOGO_SIZE),
            text=""
        )
        head_logo.grid(column=0, row=0)
        del img

        head_label = CTkLabel(self, text=self.LABEL_TEXT, font=bold15)
        head_label.grid(column=0, row=1, pady=(5, 0))


class MainFrame(CTkFrame):
    PLACE_HOLDER = 'Name of your venv'
    ENV_NAME = 'Environment name :'
    ENV_DIR = 'Project path :'
    BROWSE_BTN_TEXT = 'BROWSE'
    CREATE_BTN_TEXT = 'Create your Virtual Env'

    def __init__(self, master: CTk):
        super().__init__(master, fg_color= const.COLOR_TRANSPARENT)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        frame_name = CTkFrame(self, fg_color=const.COLOR_TRANSPARENT)
        frame_name.grid(column=0, row=0, pady=(15, 30))

        env_name_label = CTkLabel(frame_name, text=self.ENV_NAME, font=bold12)
        env_name_label.grid(column=0, row=0)

        self.env_name_entry = CTkEntry(frame_name, width=const.ENTRY_WIDTH, placeholder_text=self.PLACE_HOLDER, font=bold12)
        self.env_name_entry.grid(column=1, row=0, padx=(20, 0))

        dir_frame = CTkFrame(self, fg_color=const.COLOR_TRANSPARENT)
        dir_frame.grid(column=0, row=1, pady=(0, 40))

        env_dir_label = CTkLabel(dir_frame, text=self.ENV_DIR, font=bold12)
        env_dir_label.grid(column=0, row=0)

        self.env_dir_entry = CTkEntry(dir_frame, width=const.ENTRY_WIDTH, state='disabled', font=bold12)
        self.env_dir_entry.grid(column=1, row=0, padx=(20, 20))

        self.browse_btn = CTkButton(dir_frame, text=self.BROWSE_BTN_TEXT, width=85, font=bold15)
        self.browse_btn.grid(column=2, row=0)

        self.create_btn = CTkButton(self, text=self.CREATE_BTN_TEXT, font=bold15)
        self.create_btn.grid(column=0, row=2, pady=(0, 1))

    def set_btn_state(self, new_state: str) -> None:
        self.browse_btn.configure(state=new_state)
        self.create_btn.configure(state=new_state)

    def reset_entries(self):
        self.env_name_entry.delete(0, 'end')
        self.env_name_entry.configure(placeholder_text=self.PLACE_HOLDER)

        self.env_dir_entry.configure(state= 'normal')
        self.env_dir_entry.delete(0, 'end')
        self.env_dir_entry.configure(state= 'disabled')


class PopUp(CTkToplevel):
    FADE_DURATION = const.POP_UP_FADE_DURATION
    TITLE = const.APP_TITLE
    LABEL1_TEXT = 'Python virtual environment:'
    LABEL2_TEXT ='Wait creation in progress ...'

    def __init__(self, master: CTk, work_area:dict[str, int], icon_path: str):
        super().__init__(master)

        if sys.platform.startswith('win'):
            self.iconbitmap(default=icon_path)
            self.after(200, lambda: self.iconbitmap(icon_path)) # Just to fix bug on customtkinter

        self.title(self.TITLE)
        self.lift()                       # Lift window on top
        self.overrideredirect(True)       # Hide title bar.
        self.attributes('-topmost', True) # Stay on top.
        self.attributes('-alpha', 0)      # Avoid white flickering of background.
        transparent_color = self._apply_appearance_mode(self.cget("fg_color"))
        self.attributes("-transparentcolor", transparent_color)
        self.config(background=transparent_color)

        self.after(25, self.fade_in)      # Avoid white flickering of background.

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame = CTkFrame(self, width=const.POP_UP_W, height=const.POP_UP_H, border_width=const.POP_UP_BORDER_W)
        self.frame.grid()
        self.frame.grid_propagate(False)
        self.frame.grid_columnconfigure(0, weight=1)
        self.geometry(self.create_geometry(const.POP_UP_W, const.POP_UP_H, work_area, const.POP_UP_Y_OFFSET))

        CTkLabel(self.frame, text=self.LABEL1_TEXT, font=bold18, fg_color=const.COLOR_TRANSPARENT).grid(column=0, row=0, pady=(20, 0))
        CTkLabel(self.frame, text=self.LABEL2_TEXT, font=bold15).grid(column=0, row=1, pady=(20, 20))

        self.progressbar = CTkProgressBar(self.frame, orientation="horizontal", mode='indeterminate')
        self.progressbar.grid(column=0, row=2)
        self.progressbar.set(0)
        self.progressbar.start()

        self.grab_set()

    def create_geometry(self, width: int, height: int, work_area: dict[str, int], y_offset:int = 0) -> str:
        x = (work_area['width'] - width) // 2
        y = (work_area['height'] - height) // 2
        return f"{width}x{height}+{x}+{y + y_offset}"

    def fade_in(self):
        for i in range(0,110,10):
            if not self.winfo_exists():
                break
            self.attributes('-alpha', i/100)
            self.update()
            t_sleep(1/self.FADE_DURATION)

    def fade_out(self):
        for i in range(100,0,-10):
            if not self.winfo_exists():
                break
            self.attributes('-alpha', i/100)
            self.update()
            t_sleep(1/self.FADE_DURATION)

    def on_closing(self) -> None:
        self.fade_out()
        self.grab_release()
        self.destroy()

        if self.master:
            self.master.focus_force()


class App():
    TITLE = const.APP_TITLE
    FADE_DURATION = const.POP_UP_FADE_DURATION
    COPYRIGHT = 'Slewog Software @ All Rights Reserved'
    SUCCESS_MSG = 'Your virtual environment has been created'
    ERROR_MSG = 'Sorry we can\'t create your virtual environment'
    BAD_PATH_MSG = 'Select a valid directory to create your virtual environment'
    BAD_NAME_MSG = 'Please enter a valid name for your virtual environment'
    CLOSE_MSG = 'Do you want to close the program?'

    def __init__(self, window: CTk, display_work_area: dict[str, int]):
        self.display_work_area = display_work_area
        self.project_dir: str = ''
        self.venv_name: str = ''
        self.master_w = window

        window.bind('<Escape>', lambda e: self.on_closing)
        window.protocol('WM_DELETE_WINDOW', self.on_closing)

        window.title(const.APP_TITLE)
        if sys.platform.startswith('win'):
            window.iconbitmap(os_path_join(ASSETS_PATH, const.APP_ICON))
        window.resizable(width=const.APP_RESIZABLE, height=const.APP_RESIZABLE)
        window.geometry(self.create_geometry(const.APP_W, const.APP_H))
        window.grid_columnconfigure(0, weight=1)

        self.header = HeaderFrame(window)
        self.header.grid(column=0, row=0, pady=(15, 20))

        self.main = MainFrame(window)
        self.main.grid(column=0, row=1, sticky='ew', padx=10)
        self.main.browse_btn.configure(command=self.set_dir_project)
        self.main.create_btn.configure(command=self.check_venv_param)

        copyright = CTkLabel(window, text=self.COPYRIGHT, font=bold12_under)
        copyright.grid(column=0, row=3, pady=(30, 0))

    def show_message(self, message:str, icon:str = 'warning', **kwargs) -> str | None:
        """Show a message to the user.

        Args:
            icon = 'warning' | 'question' | 'cancel' | 'check' | 'info'
        """
        msg = CTkMessagebox(title=self.TITLE, message=message, icon=icon, sound=True, fade_in_duration=self.FADE_DURATION, **kwargs)
        return msg.get()

    def set_dir_project(self):
        self.main.env_dir_entry.configure(state= 'normal')
        self.main.env_dir_entry.delete(0, 'end')
        self.main.env_dir_entry.insert(0, ctk_file_dialog.askdirectory())
        self.main.env_dir_entry.configure(state= 'disabled')

    def close_pop_up(self, success):
        self.pop_up.progressbar.stop()
        t_sleep(0.35)
        self.pop_up.on_closing()

        self.show_message(self.SUCCESS_MSG if success else self.ERROR_MSG, 'check' if success else 'cancel')

        if success:
            self.main.reset_entries()
            self.project_dir = ''
            self.venv_name = ''
        self.main.set_btn_state('normal')

    def genere_venv(self):
        os_goto_dir(self.project_dir)
        t_sleep(0.25)
        success = True if sb_run(f'python -m venv .{self.venv_name}', shell=True).returncode == 0 else False
        os_goto_dir(DIR_PATH)
        self.master_w.after(250, self.close_pop_up, success)

    def check_venv_param(self):
        self.main.set_btn_state('disabled')

        project_dir = self.main.env_dir_entry.get()
        venv_name = self.main.env_name_entry.get()

        if not os_path_isdir(project_dir):
            self.show_message(message=self.BAD_PATH_MSG)
            self.main.set_btn_state('normal')
            return

        if len(venv_name) == 0 or ' ' in venv_name or '-' in venv_name:
            self.show_message(message=self.BAD_NAME_MSG)
            self.main.set_btn_state('normal')
            return

        self.project_dir = project_dir
        self.venv_name = venv_name

        self.pop_up = PopUp(self.master_w, self.display_work_area, os_path_join(ASSETS_PATH, const.APP_ICON))
        task = Thread(target=self.genere_venv)
        task.start()

    def on_closing(self):
        response = self.show_message(message=self.CLOSE_MSG, icon='question',  option_1="No", option_2="Yes", button_width=50)
        if response == "Yes":
            self.master_w.destroy()
            return

    def create_geometry(self, app_width: int, app_height: int) -> str:
        x = (self.display_work_area['width'] - app_width) // 2
        y = (self.display_work_area['height'] - app_height) // 2
        return f"{app_width}x{app_height}+{x}+{y}"


if __name__ == '__main__':
    window = CTk()
    bold12_under = CTkFont(family=const.FONT_FAMILY, size=12, weight=const.FONT_WEIGHT, underline=True)
    bold12 = CTkFont(family=const.FONT_FAMILY, size=12, weight=const.FONT_WEIGHT)
    bold15 = CTkFont(family=const.FONT_FAMILY, size=15, weight=const.FONT_WEIGHT)
    bold18 = CTkFont(family=const.FONT_FAMILY, size=18, weight=const.FONT_WEIGHT)

    app = App(window, get_display_work_area())
    window.mainloop()
    sys.exit()