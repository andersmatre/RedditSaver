"""PyQt5 GUI Utilities

Module containing a collection of useful function to clean up code
when working with the library 'PyQt5'.
"""


from PyQt5 import QtWidgets, QtCore, QtGui


def create_label(x, y, width, height, window, font=None, font_size=14, string="", visible=True, image=None):
    label = QtWidgets.QLabel(window)
    label.setGeometry(QtCore.QRect(x, y, width, height))
    if image:
        label.setPixmap(QtGui.QPixmap(image))
    if not visible:
        label.hide()
    if font:
        font.setPointSize(font_size)
        label.setFont(font)
        label.setText(string)
    return label


def create_button(x, y, width, height, window, font=None, font_size=14, string="", visible=True):
    button = QtWidgets.QPushButton(window)
    button.setGeometry(QtCore.QRect(x, y, width, height))
    button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    if not visible:
        button.hide()
    if font:
        font.setPointSize(font_size)
        button.setFont(font)
        button.setText(string)
    return button


def create_checkbox(x, y, width, height, window, font=None, font_size=12, checked=False, string=""):
    checkbox = QtWidgets.QCheckBox(window)
    checkbox.setGeometry(QtCore.QRect(x, y, width, height))
    checkbox.setChecked(checked)
    if font:
        font.setPointSize(font_size)
        checkbox.setFont(font)
        checkbox.setText(string)
    return checkbox


def create_combobox(x, y, width, height, window, font=None, font_size=14, items=None):
    combobox = QtWidgets.QComboBox(window)
    combobox.setGeometry(QtCore.QRect(x, y, width, height))
    combobox.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
    if font:
        font.setPointSize(font_size)
        combobox.setFont(font)
        if items:
            for item in items:
                combobox.addItem(item)
    return combobox


def create_tabwindow(x, y, width, height, window, font=None,  font_size=12, tabs=None):
    tabwindow = QtWidgets.QTabWidget(window)
    tabwindow.setGeometry(QtCore.QRect(x, y, width, height))
    if font:
        font.setPointSize(font_size)
        tabwindow.setFont(font)
    tabwidgets = []
    if tabs:
        for tab in tabs:
            _tab = QtWidgets.QWidget()
            tabwindow.addTab(_tab, str(tab))
            tabwidgets.append(_tab)
        tabwindow.setCurrentIndex(0)
    yield tabwindow
    for tab in tabwidgets:
        yield tab


def create_list(x, y, width, height, window, font=None, font_size=14,):
    listwidget = QtWidgets.QListWidget(window)
    listwidget.setGeometry(QtCore.QRect(x, y, width, height))
    if font:
        font.setPointSize(font_size)
        listwidget.setFont(font)
    return listwidget


def create_spinbox(x, y, width, height, window, font=None, font_size=14, start=100, step=10, limit=1000):
    spinbox = QtWidgets.QSpinBox(window)
    spinbox.setGeometry(QtCore.QRect(x, y, width, height))
    if font:
        font.setPointSize(font_size)
        spinbox.setFont(font)
    spinbox.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
    spinbox.setMaximum(limit)
    spinbox.setSingleStep(step)
    spinbox.setProperty("value", start)
    return spinbox


def create_textfield(x, y, width, height, window, font=None, font_size=14, string=None, placeholder=None, line=False):
    if line:
        textfield = QtWidgets.QLineEdit(window)
    else:
        textfield = QtWidgets.QTextEdit(window)
    textfield.setGeometry(QtCore.QRect(x, y, width, height))
    if font:
        font.setPointSize(font_size)
        if string:
            textfield.setText(string)
        if placeholder:
            textfield.setPlaceholderText(placeholder)
    return textfield


def create_progressbar(x, y, width, height, window, visible=True):
    progressbar = QtWidgets.QProgressBar(window)
    progressbar.setGeometry(QtCore.QRect(x, y, width, height))
    progressbar.setProperty("value", 0)
    progressbar.setAlignment(QtCore.Qt.AlignCenter)
    progressbar.setTextVisible(True)
    progressbar.setOrientation(QtCore.Qt.Horizontal)
    progressbar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
    progressbar.setFormat("%p%")
    if not visible:
        progressbar.hide()
    return progressbar
