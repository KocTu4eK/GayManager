import sys
import time
from keyboard import add_hotkey
from pyautogui import getActiveWindowTitle

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWinExtras import QtWin
from PyQt5.QtCore import QSharedMemory, QTimer

from gay_manager import GayManager


if __name__ == '__main__':
    shared = QSharedMemory("5a8912df-f34c-4ba6-ab1a-8783cc36e0d1")
    if not shared.create(512, QSharedMemory.ReadWrite): sys.exit(0)

    app = QApplication(sys.argv)
    QtWin.setCurrentProcessExplicitAppUserModelID("GayManager")

    window = GayManager("accounts.json")
    window.show()
    QTimer.singleShot(1000, lambda: window.hide())

    add_hotkey("alt+k", lambda: window.focus_window()
        if getActiveWindowTitle() == "Genshin Impact" else None)

    sys.exit(window.exec_wrapper(app))
