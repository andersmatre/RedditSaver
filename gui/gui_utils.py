"""GUI Utilities

This file contains some useful utilitie functions when working with
a GUI application.
"""


import tkinter.filedialog
import tkinter
import os
import sys


def get_path(textfield=None):
    """
    Simple function to open a filedialog window
    and return the selected path.

    :keyword textfield: if given it will set the textfields
                        text to the path instead of returning it
    :return selected path:
    """
    root = tkinter.Tk()
    root.withdraw()
    path = tkinter.filedialog.askdirectory(parent=root, initialdir="/", title='Please select a directory')
    if path:
        if textfield:
            textfield.setText(path)
        else:
            return path


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def get_queue(queue):
    """
    Simple function to return every item in a queue object
    as a list.
    :param queue:
    :return a list of the queue:
    """
    result_list = []
    while not queue.empty():
        result_list.append(queue.get())
    return result_list
