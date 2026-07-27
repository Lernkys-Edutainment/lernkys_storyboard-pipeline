from pathlib import Path
import tkinter as tk
from tkinter import filedialog


def select_folder(title: str) -> Path:
    """
    Opens a native folder selection dialog.

    Args:
        title:
            Title displayed on the folder picker.

    Returns:
        Path object representing the selected folder.

    Raises:
        ValueError:
            If no folder was selected.
    """

    root = tk.Tk()

    # Hide the blank tkinter window
    root.withdraw()

    # Keep dialog above all windows
    root.attributes("-topmost", True)

    folder = filedialog.askdirectory(
        title=title
    )

    root.destroy()

    if not folder:
        raise ValueError("No folder selected.")

    return Path(folder)