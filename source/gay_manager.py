import json
from copy import deepcopy
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

from config import Config
from button_handler import ButtonHandler
import resources


class GayManager(QtWidgets.QMainWindow):
    def __init__(self, filename):
        super(GayManager, self).__init__()

        self.create_window()
        self.create_tray_icon()

        for display_name in Config.load(filename):
            self.show_account(display_name)

    def create_window(self):
        self.setFixedSize(260, 370)
        self.frameGeometry().moveCenter(QtWidgets.QDesktopWidget().availableGeometry().center())
        self.setWindowTitle("Gay Manager")
        self.setWindowIcon(QIcon(":/icons/icon"))

        # Accounts
        self.accounts = QtWidgets.QListWidget(self)
        self.accounts.setFixedSize(240, 314)
        self.accounts.move(10, 10)
        self.accounts.setStyleSheet("border-width: 1px; border-color: black; border-style: solid;");

        # Confirm
        btn_confirm = QtWidgets.QPushButton(self)
        btn_confirm.setText("Confirm")
        btn_confirm.setFont(QFont("Consolas", 13))
        btn_confirm.setFixedWidth(98)
        btn_confirm.move(10, 330)
        btn_confirm.setStyleSheet("background: white; border-width: 1px; border-color: black; border-style: solid; border-radius: 5;")
        btn_confirm.clicked.connect(lambda: ButtonHandler.confirm(self))

        # Remove
        btn_remove = QtWidgets.QPushButton(self)
        btn_remove.setText("Remove")
        btn_remove.setFont(QFont("Consolas", 13))
        btn_remove.setFixedWidth(98)
        btn_remove.move(113, 330)
        btn_remove.setStyleSheet("background: rgb(255, 60, 60); border-width: 1px; border-color: black; border-style: solid; border-radius: 5;")
        btn_remove.clicked.connect(lambda: ButtonHandler.remove(self))

        # +
        btn_add = QtWidgets.QPushButton(self)
        btn_add.setText("+")
        btn_add.setFont(QFont("Consolas", 16))
        btn_add.setFixedWidth(34)
        btn_add.move(216, 330)
        btn_add.setStyleSheet("background: white; border-width: 1px; border-color: black; border-style: solid; border-radius: 5;")
        btn_add.clicked.connect(lambda: ButtonHandler.add(self))

    def create_tray_icon(self):
        self.tray_icon = QtWidgets.QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(":/icons/icon"))

        quit_action = QtWidgets.QAction("Exit", self)
        quit_action.setIcon(QIcon(":/icons/exit"))
        quit_action.triggered.connect(QtWidgets.qApp.quit)

        tray_menu = QtWidgets.QMenu()
        tray_menu.addAction(quit_action)

        self.tray_icon.activated.connect(lambda reason: self.focus_window() if reason == 3 else None)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def focus_window(self):
        self.show(), # case: hidden
        self.setFocus(), # case: on the background
        self.activateWindow(), # case: on the background
        self.setWindowState(Qt.WindowNoState) # case: minimized

    def show_account(self, display_name):
        if len(display_name) > 21: # abobaxyzqwerty@example.com —> abobaxyz*****mple.com
            display_name_old = deepcopy(display_name)
            display_name = f"{display_name[:8]}*****{display_name[len(display_name) - 8:]}"
            Config.add(display_name, Config.get(display_name_old))
            Config.remove(display_name_old)

        if len(self.accounts.findItems(display_name, Qt.MatchExactly)) > 0: return

        if self.accounts.count() > 0: # shitcode xd
            delimiter = QtWidgets.QListWidgetItem("——————————————————————————————————————————————————————————————————————————————————————————————————————————————————")
            delimiter.setFont(QFont("Arial", 1))
            self.accounts.addItem(delimiter)

        qItem = QtWidgets.QListWidgetItem(display_name)
        qItem.setFont(QFont("Consolas", 14))
        self.accounts.addItem(qItem)

        if self.accounts.count() > 21: # supershitcode xd
            for i in range(self.accounts.count()):
                item = self.accounts.item(i)
                if item.text() == "——————————————————————————————————————————————————————————————————————————————————————————————————————————————————":
                    item.setText("——————————————————————————————————————————————————————————————————————————————————————————————————————————")

    def hide_account(self):
        current_row = deepcopy(self.accounts.currentRow())
        hidden_display_name = None

        if current_row + 1 == self.accounts.count(): # last
            hidden_display_name = self.accounts.takeItem(current_row).text()
            self.accounts.takeItem(current_row - 1)
        else:
            self.accounts.takeItem(current_row + 1)
            hidden_display_name = self.accounts.takeItem(current_row).text()

        return hidden_display_name

    def exec_wrapper(self, app):
        app.exec_()
        Config.save() # save on exit

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        Config.save() # save on hide
