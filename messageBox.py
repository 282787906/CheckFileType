import tkinter.messagebox

from tkinter import *
import time
import winsound
def play_music():
    winsound.PlaySound('SystemAsterisk', winsound.SND_ASYNC)
    # winsound.PlaySound('SystemExclamation', winsound.SND_ASYNC)
    # winsound.PlaySound('SystemExit', winsound.SND_ASYNC)
    # winsound.PlaySound('SystemHand', winsound.SND_ASYNC)
    # winsound.PlaySound('SystemQuestion', winsound.SND_ASYNC)
    # sounds = ["-1", "MB_ICONASTERISK", "MB_ICONEXCLAMATION", "MB_ICONHAND", "MB_ICONQUESTION", "winsound.MB_OK"]
    # for i in sounds:
    #     try:
    #         winsound.Beep(1600, 500)
    time.sleep(2)
    #         winsound.MessageBeep(eval(i))
    #     except RuntimeError and NameError:
    #         print("no {} messagebeep".format(i))
    #     else:
    #         print("has the sound flag{}".format(i))

def showErrorMsg(title,msg):
    tkinter.messagebox.showwarning( title,msg)
def play_beep():
    # winsound.Beep(600, 1000)
    sounds = ["-1", "MB_ICONASTERISK", "MB_ICONEXCLAMATION", "MB_ICONHAND", "MB_ICONQUESTION", "winsound.MB_OK"]
    for i in sounds:
        try:
            winsound.Beep(1600, 500)
            time.sleep(2)
            winsound.MessageBeep(eval(i))
        except RuntimeError and NameError:
            print("no {} messagebeep".format(i))
        else:
            print("has the sound flag{}".format(i))


if __name__ == "__main__":
    play_music()