"""RedditSaver Main Script

This script contains the main function to the RedditSaver project.
When ran it will launch an instance of the RedditGui class.
"""


from gui.reddit_gui import RedditGui
from PyQt5 import QtWidgets
import sys


def main():
    """Creates an instance of the RedditGui class and launches it."""
    app = QtWidgets.QApplication(sys.argv)

    ui = RedditGui(size=(690, 750), window_title="RedditSaver by Anders Matre", logo="./assets/redditlogo.png")
    ui.widgets()
    ui.buttons()
    ui.window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
