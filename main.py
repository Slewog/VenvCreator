import sys
import customtkinter as ctk


class App(ctk.CTk):
    def __init__(self, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs)

if __name__ == '__main__':
    app = App()
    app.mainloop()
    sys.exit()