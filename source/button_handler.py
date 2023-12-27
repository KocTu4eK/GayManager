import pyautogui
import pyperclip
from time import sleep

from PyQt5.QtWidgets import QMessageBox, QDialog, QLineEdit, QDialogButtonBox, QFormLayout
from PyQt5.QtGui import QIcon

from config import Config
import resources


class ButtonHandler:
    def confirm(window):
        if window.accounts.currentRow() % 2 == 0:
            window.hide() # hide in tray

            account = Config.get(window.accounts.currentItem().text())
            pixel_normal = pyautogui.pixel(96, 987)

            pyautogui.click(1823, 983, duration=0.1, tween=pyautogui.easeInOutQuad) # logout
            sleep(0.05)
            pyautogui.click(1080, 560, duration=0.1, tween=pyautogui.easeInOutQuad) # confirm
            sleep(0.05)

            while True:
                if pyautogui.pixel(96, 987) != pixel_normal: break

            pyautogui.click(900, 450, duration=0.1, tween=pyautogui.easeInOutQuad) # login field
            sleep(0.05)
            pyperclip.copy(account["login"])
            pyautogui.hotkey("ctrl", "v") # login input
            sleep(0.05)
            pyautogui.click(900, 520, duration=0.1, tween=pyautogui.easeInOutQuad) # password field
            sleep(0.05)
            pyperclip.copy(account["password"])
            pyautogui.hotkey("ctrl", "v") # password input
            sleep(0.05)
            pyautogui.click(950, 670, duration=0.1, tween=pyautogui.easeInOutQuad) # start game

    def remove(window):
        if window.accounts.currentRow() % 2 == 0:
            modal = QMessageBox()
            modal.setWindowTitle("Confirmation")
            modal.setWindowIcon(QIcon(":/icons/icon"))
            modal.setText(f"Are you sure you want to delete this account?\nSelected account: '{window.accounts.currentItem().text()}'")
            modal.setIcon(QMessageBox.Warning)
            modal.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            modal.buttonClicked.connect(lambda btn: Config.remove(window.hide_account()) if btn.text() == "OK" else None)
            modal.exec_()

    def add(window):
        dialog = QDialog(window)

        display_name = QLineEdit(dialog)
        login = QLineEdit(dialog)
        password = QLineEdit(dialog)

        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        button_box.accepted.connect(lambda: dialog.accept() if display_name.text() != "" and login.text() != "" and password.text() != "" else None)
        button_box.rejected.connect(dialog.reject)

        layout = QFormLayout(dialog)
        layout.addRow("Display name:", display_name)
        layout.addRow("Login / e-mail:", login)
        layout.addRow("Password:", password)
        layout.addWidget(button_box)

        dialog.setWindowTitle("Add a new account")
        dialog.setLayout(layout)

        if dialog.exec():
            Config.add(display_name.text(), {
                "login": login.text(),
                "password": password.text()
            })
            window.show_account(display_name.text())
