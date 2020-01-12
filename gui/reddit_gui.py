"""Reddit Gui

Module containing the Reddit Gui class that inherits from the
Gui class to create a Gui to the save_reddit().
"""


from PyQt5 import QtWidgets, QtGui
from queue import Queue
import time
import os
from gui.gui_utils import get_queue
from logic.stoppable_thread import StoppableThread
from logic.save_subreddit import save_subreddit
from logic.verify_inputs import verify_inputs
from gui.gui_utils import get_path
from gui.gui_widgets import create_label, create_button, create_checkbox, \
    create_combobox, create_tabwindow, create_list, create_spinbox, create_textfield, \
    create_progressbar


# TODO, add a login form to save reddit with own user
# TODO, add a stop functionality to the scraping thread (hard)


class RedditGui:
    """Reddit Saver GUI class

    A GUI class that is used in conjunction with the save_subreddit()
    to create a simple GUI for said function.
    """
    def __init__(self, size=(100, 100), font="Verdana", window_title="Title", logo=None):

        self.window = QtWidgets.QMainWindow()
        self.window_widget = QtWidgets.QWidget(self.window)

        self.window.setCentralWidget(self.window_widget)
        self.window.setWindowTitle(window_title)
        self.window.setFixedSize(size[0], size[1])
        self.window.setWindowIcon(QtGui.QIcon(logo))

        self.font = QtGui.QFont()
        self.font.setFamily(font)
        self.font.setPointSize(12)

        self.queue = Queue(maxsize=0)
        queue_thread = StoppableThread(target=self.process_queue, args=([self.queue]), daemon=True)
        queue_thread.start()

    def widgets(self):  # TODO, clean this up
        """Creates GUI widgets"""
        self.tab, self.inputs, self.outputs, self.results = create_tabwindow(50, 170, 591, 521, window=self.window_widget,
                                                                             font=self.font, tabs=["Inputs", "Outputs", "Results"])
        self.saveimages_checkbox = create_checkbox(154, 350, 150, 40, window=self.inputs,
                                                   font=self.font, checked=True, string="Save Images", )
        self.savecsv_checkbox = create_checkbox(330, 350, 150, 40, window=self.inputs,
                                                font=self.font, checked=True, string="Save CSV", )
        self.subredditfolder_checkbox = create_checkbox(50, 250, 400, 21, window=self.outputs,
                                                        font=self.font, checked=True,
                                                        string="Automatically create folder for each subreddit", )
        self.header_label = create_label(150, 60, 450, 60, window=self.window_widget,
                                         font=self.font, font_size=36, string="RedditSaver")
        self.subreddit_label = create_label(120, 50, 150, 21, window=self.inputs,
                                            font=self.font, string="Subreddit")
        self.amount_label = create_label(120, 130, 150, 21, window=self.inputs,
                                         font=self.font, string="Amount")
        self.sort_label = create_label(310, 50, 150, 21, window=self.inputs,
                                       font=self.font, string="Sort by")
        self.keywords_label = create_label(120, 210, 150, 21, window=self.inputs,
                                           font=self.font, string="Keywords")
        self.time_label = create_label(310, 130, 150, 21, window=self.inputs,
                                       font=self.font, string="Time")
        self.imagefolder_label = create_label(60, 60, 200, 25, window=self.outputs,
                                              font=self.font, font_size=12, string="Image Folder Path: ")
        self.csvfolder_label = create_label(60, 140, 200, 25, window=self.outputs,
                                            font=self.font, font_size=12, string="CSV Folder Path: ")
        self.invalid_label = create_label(223, 440, 200, 50, window=self.inputs,
                                          font=self.font, string="Invalid Inputs", visible=False)
        self.imagefolder_textfield = create_textfield(50, 90, 400, 30, window=self.outputs,
                                                      font=self.font, font_size=12,
                                                      string=os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'))
        self.csvfolder_textfield = create_textfield(50, 170, 400, 30, window=self.outputs,
                                                    font=self.font, font_size=12,
                                                    string=os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'))
        self.stop_button = create_button(180, 400, 221, 50, window=self.inputs,
                                         font=self.font, string="Stop", visible=False)
        self.start_button = create_button(180, 400, 221, 50, window=self.inputs,
                                          font=self.font, string="Start")
        self.imagefolder_button = create_button(460, 90, 80, 30, window=self.outputs,
                                                font=self.font, font_size=10, string="Change")
        self.csvfolder_button = create_button(460, 170, 80, 30, window=self.outputs,
                                              font=self.font, font_size=10, string="Change")
        self.results_list = create_list(60, 120, 458, 200, window=self.results, font=self.font)
        self.time_combobox = create_combobox(310, 160, 151, 31, window=self.inputs, font=self.font,
                                             items={"All": 0, "Hour": 1, "Day": 2, "Week": 3, "Month": 4, "Year": 5})
        self.sort_combobox = create_combobox(310, 80, 151, 31, window=self.inputs, font=self.font,
                                             items={"Top": 0, "Hot": 1, "New": 2, "Controversial": 3, "Trending": 4})
        self.amount_spinbox = create_spinbox(120, 160, 151, 31, window=self.inputs, start=200)
        self.subreddit_textfield = create_textfield(120, 80, 151, 31, window=self.inputs, font=self.font,
                                                    placeholder="CozyPlaces", line=True)
        self.keywords_textfield = create_textfield(120, 240, 341, 100, window=self.inputs, font=self.font,
                                                   placeholder="snow, morning, coffee")
        self.progressbar = create_progressbar(50, 130, 591, 30, window=self.window_widget, visible=False)
        self.reddit_image = create_label(50, 20, 100, 100, window=self.window_widget, image="./assets/redditlogofull.png")

    def buttons(self):
        """Connects buttons to functions"""
        self.start_button.clicked.connect(self.start_save)
        self.stop_button.clicked.connect(self.stop_save)
        self.imagefolder_button.clicked.connect(lambda: get_path(textfield=self.imagefolder_textfield))
        self.csvfolder_button.clicked.connect(lambda: get_path(textfield=self.csvfolder_textfield))

    def start_save(self):
        """Calls save_subreddit() with current settings

        First checks if user inputs are valid by calling verify_inputs()
        and then takes the user inputs and creates a thread that calls the
        save_subreddit() with said inputs.
        """
        inputs = {"client_id": None,  # Needs valid information to work
                  "client_secret": None,
                  "user_agent": None,  # Needs valid information to work
                  "subreddit": self.subreddit_textfield.toPlainText(),
                  "sort": str(self.sort_combobox.currentText()).lower(),
                  "time": str(self.time_combobox.currentText()).lower(),
                  "amount": int(self.amount_spinbox.value()),
                  "min_score": 0,
                  "max_score": 999999999,
                  "save_img": self.saveimages_checkbox.isChecked(),
                  "save_csv": self.savecsv_checkbox.isChecked(),
                  "keywords": self.keywords_textfield.toPlainText().split(","),
                  "imagepath": self.imagefolder_textfield.toPlainText(),
                  "csvpath": self.csvfolder_textfield.toPlainText(),
                  "subfolder": self.subredditfolder_checkbox.isChecked(),
                  "queue": self.queue}

        if verify_inputs(**inputs):
            self.save_thread = StoppableThread(target=save_subreddit, kwargs=inputs, daemon=True)
            self.save_thread.start()
            self.results_list.clear()
            self.progressbar.setProperty("value", 0)
            self.start_button.hide()
            self.invalid_label.hide()
            self.stop_button.show()
            self.progressbar.show()
        else:
            self.invalid_label.show()

    def stop_save(self):  # FIXME, this doesn't actually do anything other than changing the GUI
        """Changes the GUI to indicate that the saving process has been terminated"""
        self.stop_button.hide()
        self.start_button.show()
        self.progressbar.hide()

    def process_queue(self, queue):
        """Processes the given queue

        Normally called in a thread when the GUI launches to
        continuously listen for updates in the given queue and act accordingly.
        """
        clear = 0
        while True:
            time.sleep(0.2)
            queue_list = get_queue(queue)
            for entry in queue_list:
                if type(entry) is dict:
                    for key in entry:
                        if key == "progress":
                            self.progressbar.setProperty("value", entry[key])
                        else:
                            self.stop_save()
                            self.results_list.addItem(QtWidgets.QListWidgetItem(f"{key}: {entry[key]}"))
            if self.invalid_label.isVisible():
                print(clear)
                clear += 1
                if clear > 20:
                    self.invalid_label.hide()
                    clear = 0
