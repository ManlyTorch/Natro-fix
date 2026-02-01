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

fixedVersions = {
    "bc1e28f4be1f4266": "v1",
    "ecc9c250281b4c14": "og",
    "061a1e42291f47eb": "og",
    "a24f7de245e949c3": "v2",
    "1588a9c58c674e38": "v2",
    "889d2588b25a43d1": "v2",
}

def getPath(relativePath):
    base_path = ""
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relativePath)

def get_folder():
    root = tk.Tk()
    root.withdraw()  # hide the main window
    folder_path = filedialog.askdirectory(title="Select a folder")
    root.destroy()
    return folder_path

if result.stdout and result.stdout.count("version-") == 1:
    version = result.stdout.split("version-")[1].replace("\n", "")

    if not fixedVersions[version]:
        # --- UI ---
        root = tk.Tk()

        style = ttk.Style(root)
        style.theme_use("clam")
        
        frame = ttk.Frame(root, padding=10)
        frame.pack(fill="both", expand=True)

        result_label = ttk.Label(
            frame,
            text="Unknown version please contact somebody"
        )
        result_label.pack(pady=5)

        root.mainloop()
    else:
        path = get_folder()
        
        if path.count("nm_image_assets") >= 1:
            path = str(Path(path).parent)

        dst1 = os.path.join(path + "/nm_image_assets/offset/bitmaps.ahk")
        dst2 = os.path.join(path + "/nm_image_assets/inventory/bitmaps.ahk")

        offsetbitmap = offsetFix = shutil.copyfile(getPath("bitmaps\\" + fixedVersions[version] + "offsetFix.ahk"), dst1)
        planterbitmap = planterFix = shutil.copyfile(getPath("bitmaps\\" + fixedVersions[version] + "planterFix.ahk"), dst2)

        # --- UI ---
        root = tk.Tk()

        style = ttk.Style(root)
        style.theme_use("clam")

        frame = ttk.Frame(root, padding=10)
        frame.pack(fill="both", expand=True)

        result_label = ttk.Label(
            frame,
            text="Should be fixed"
        )
        result_label.pack(pady=5)

        root.mainloop()
else:
    # --- UI ---
    root = tk.Tk()

    style = ttk.Style(root)
    style.theme_use("clam")

    frame = ttk.Frame(root, padding=10)
    frame.pack(fill="both", expand=True)

    result_label = ttk.Label(
        frame,
        text="Incorrect version, program won't work"
    )
    result_label.pack(pady=5)

    root.mainloop()
