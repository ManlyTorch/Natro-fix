import subprocess
import sys
import os
import shutil
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pathlib import Path

cmd = [
    "reg",
    "query",
    r"HKCR\roblox\shell\open\command",
    "/v",
    "version"
]

result = subprocess.run(
    cmd,
    capture_output=True,
    text=True,
    shell=False
)

def getPath(relativePath):
    base_path = ""
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relativePath)

def get_folder():
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Select a folder")
    root.destroy()
    return folder_path

def showText(text: str):
    root = tk.Tk()

    style = ttk.Style(root)
    style.theme_use("clam")

    frame = ttk.Frame(root, padding=10)
    frame.pack(fill="both", expand=True)

    result_label = ttk.Label(
        frame,
        text=text
    )
    result_label.pack(pady=5)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    x = (screen_width // 2) - (150)
    y = (screen_height // 2) - (25)
    
    root.geometry(f"{350}x{50}+{x}+{y}")

    root.attributes("-topmost", True)

    root.mainloop()

def attempt_fix(version: str):
    path = get_folder()
    roblox_version_path = os.environ["LOCALAPPDATA"] + r"\Roblox\Versions\version-" + version
    if not os.path.exists(roblox_version_path):
        showText("Roblox version folder not found, please contact me!")
        return

    roblox_version_path = roblox_version_path + r"\content\fonts"

    if not path:
        return

    if path.count("nm_image_assets") <= 0:
        path = path + "/nm_image_assets"

    if not os.path.exists(path + "/offset") or not os.path.exists(path + "/inventory"):
        showText("Invalid folder selected, please select natro macro folder.\nClose this window and try again.")
        attempt_fix(version)
    else:
        dst1 = os.path.join(path + "/offset/bitmaps.ahk")
        dst2 = os.path.join(path + "/inventory/bitmaps.ahk")

        offsetbitmap = offsetFix = shutil.copyfile(getPath("bitmaps\\" + "offset.ahk"), dst1)
        planterbitmap = planterFix = shutil.copyfile(getPath("bitmaps\\" + "planter.ahk"), dst2)

        fonts = shutil.copytree(getPath("fonts"), roblox_version_path, dirs_exist_ok=True)

        showText("Fix applied! If it doesn't work, it's another issue.")

if result.stdout and result.stdout.count("version-") == 1:
    version = result.stdout.split("version-")[1].replace("\n", "")

    attempt_fix(version)
else:
    showText("Roblox version not found, please make sure Roblox is installed.")
