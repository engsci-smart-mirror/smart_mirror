import tkinter
from tkinter.ttk import *


class SmartMirrorGui(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        self._frame = None
        self.switch_frame(SignInPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class SignInPage(tkinter.Frame):
    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        tkinter.Label(self, text="Welcome to your Smart mirror. Please hold still while we sign you in.")\
            .pack(side="top", pady=10)
        self.label = tkinter.Label(self)
        self.label.pack(side="top", pady=30)
        self.counter(5, master)

    def counter(self, number, master):
        self.label['text'] = number
        if number > 0:
            self.after(1000, self.counter, number-1, master)
        else:
            master.switch_frame(SetupPage)


class SetupPage(tkinter.Frame):
    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        tkinter.Label(self, text="Recognized Face.").pack(side="top", pady=10)
        name = 'Kelly'
        tkinter.Label(self, text="Hi " + name).pack(side="top", pady=10)
        tkinter.Label(self, text="Please wait while we set things up for you").pack(side="top", pady=10)
        self.progress = Progressbar(self, orient='horizontal', length=100, mode='determinate')
        self.progress.pack(pady=10)
        self.progressbar(0, master)

    def progressbar(self, number, master):
        self.progress['value'] = number
        if number != 100:
            self.after(100, self.progressbar, number+1, master)
        else:
            master.switch_frame(MainPage)


class MainPage(tkinter.Frame):
    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        tkinter.Label(self, text="This is the main page").pack(side="top", pady=10)


if __name__ == "__main__":
    GUI = SmartMirrorGui()
    GUI.mainloop()
