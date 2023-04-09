import json
import os
import re
import sys
import threading
from tkinter import *
from tkinter import messagebox

import keyboard as kbd
from pynput.keyboard import Controller
from win32 import win32gui

DEFAULT_TITLE = "BSS Hotbar Macro"
SETTINGS_PATH = "hbm-settings.json"
HB_RANGE = range(1, 8)


# noinspection PyBroadException
def load_settings():
    try:
        with open(SETTINGS_PATH, "r") as f:
            settings = json.load(f)
            s_hotbars = settings["hotbars"]
            for hb in s_hotbars.keys():
                for key in s_hotbars[hb].keys():
                    hotbars[int(hb)][key].set(s_hotbars[hb][key])
        print("Loaded settings")
    except FileNotFoundError:
        print("Settings file not found. Using default")
    except:
        print("Problem with settings file. Using default")


def save_settings():
    global hotbars

    settings = {
        "hotbars": {}
    }

    for hb in hotbars.keys():
        settings["hotbars"][hb] = {}
        for key in hotbars[hb]:
            settings["hotbars"][hb][key] = hotbars[hb][key].get()

    try:
        with open(SETTINGS_PATH, "w") as f:
            json.dump(settings, f, indent=4)
        print("Saved settings")
    except Exception as e:
        print("!! Cannot save settings")
        print(e)


# noinspection PyBroadException,PyProtectedMember
def resource_path(relative_path: str):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path: str = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def focus_roblox_window():
    window_name = "Roblox"
    handle = win32gui.FindWindow(None, window_name)
    if handle != 0:
        # minimized window handler
        if win32gui.IsIconic(handle):
            win32gui.ShowWindow(handle, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(handle)


# Initial window
root = Tk()
root.geometry("280x250")
root.resizable(False, False)
root.title(DEFAULT_TITLE)
root.iconbitmap(default=resource_path("wink.ico"))

running = False

keyboard = Controller()

with open(resource_path("version")) as file:
    VERSION = file.read()

# Credit
credit = Label(root, text=f"v{VERSION} by rens#6161", fg="gray", font=(None, 8))
credit.place(rely=1.0, relx=1.0, x=0, y=0, anchor=SE)  # fixed bottom right window

# Hotbars
hotbars = {}
for i in HB_RANGE:
    hotbars[i] = {
        "on": BooleanVar(root, value=False),
        "interval_seconds": StringVar(root, value="0")
    }


def get_hotbar_interval_seconds(hb: int):
    hotbar = hotbars[hb]
    interval_seconds = hotbar["interval_seconds"].get()
    try:
        return int(interval_seconds)
    except (Exception, ValueError):
        extract_nums = int("".join(re.findall(r"\d+", interval_seconds)) or "0")
        hotbar["interval_seconds"].set(str(extract_nums))
        return extract_nums


def get_hotbar_on(hb: int):
    hotbar = hotbars[hb]
    on = hotbar["on"].get()
    return on


hotbars_frame = Frame(highlightbackground="light gray", highlightthickness=1)
hotbars_frame.pack(padx=16, pady=12)

hotbar_widgets = {}
for i in HB_RANGE:
    hotbar = hotbars[i]

    hotbar_frame = Frame(hotbars_frame)
    hotbar_frame.pack()

    chk = Checkbutton(hotbar_frame, text=f"[{i}] every", variable=hotbar["on"])
    chk.grid(column=0, row=0)

    entry = Entry(hotbar_frame, width=4, textvariable=hotbar["interval_seconds"], validate="key")
    entry["validatecommand"] = (hotbar_frame.register(lambda s: s.isdigit()), "%S")
    entry.grid(column=1, row=0)

    hotbar_widgets[i] = {"chk": chk, "entry": entry}

    Label(hotbar_frame, text="seconds").grid(column=2, row=0)


def update_main_button_text():
    if running:
        main_button.config(text="[F8] Stop", fg="red")
        root.title("Running - " + DEFAULT_TITLE)
    else:
        main_button.config(text="[F8] Start", fg="green")
        root.title(DEFAULT_TITLE)


macro_timers = []


def loop_hotbar(hb):
    if not running:
        return

    # Filter out finished intervals from the macro_timers list
    macro_timers[:] = [t for t in macro_timers if t.is_alive()]

    print("Pressing", hb)
    keyboard.press(str(hb))
    keyboard.release(str(hb))

    timer = threading.Timer(get_hotbar_interval_seconds(hb), loop_hotbar, [hb])
    timer.start()

    macro_timers.append(timer)


def start_macro():
    for hotbar in hotbars.keys():
        if get_hotbar_on(hotbar):
            loop_hotbar(hotbar)


def stop_macro():
    root.focus()
    for timer in macro_timers:
        timer.cancel()


def toggle_macro():
    global running

    for i in HB_RANGE:
        interval_seconds = get_hotbar_interval_seconds(i)
        hotbar = hotbars[i]
        if interval_seconds <= 0:
            hotbar["interval_seconds"].set("0")
            hotbar["on"].set(False)

    atleast_one = False
    for hotbar in hotbars.values():
        if hotbar["on"].get():
            atleast_one = True
            break

    if not atleast_one:
        messagebox.showwarning(
            message="You need to enable at least one hotbar to start!"
        )
        return

    running = not running
    update_main_button_text()

    if running:
        focus_roblox_window()

    for widgets in hotbar_widgets.values():
        for widget in widgets.values():
            if running:
                widget.config(state="disabled")
            else:
                widget.config(state="normal")

    if running:
        t = threading.Timer(2, start_macro)
        t.start()
        macro_timers.append(t)
    else:
        stop_macro()
    save_settings()


kbd.on_press_key("F8", lambda _: toggle_macro())

main_button = Button(root, text="[F8] Start", command=toggle_macro, fg="green")
main_button.pack()

load_settings()


def on_close():
    global hotbars
    print("Exiting...")
    for i in HB_RANGE:
        interval_seconds = get_hotbar_interval_seconds(i)
        hotbar = hotbars[i]
        if interval_seconds <= 0:
            hotbar["interval_seconds"].set("0")
            hotbar["on"].set(False)
    save_settings()
    root.destroy()
    exit()


root.protocol("WM_DELETE_WINDOW", func=on_close)
root.mainloop()

print("Done")
