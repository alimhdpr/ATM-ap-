import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QLineEdit,
                             QVBoxLayout, QHBoxLayout, QMessageBox, QGridLayout, QStackedWidget)
from PyQt6.QtCore import Qt

users = []

class User:
    def __init__(self, pin:str, bal:float, card:str):
        self.pin = pin
        self.bal = bal
        self.card = card

with open("users.txt", "r") as file:
    for line in file:
        info = line.split()
        user = User(info[1], float(info[2]), info[3])
        users.append(user)

class Database:
    def __init__(self):
        self.user1 = users[0]
        self.user2 = users[1]


    def validate_pass(self, pin: str):
        if self.user1.pin == pin:
            return True
        return False

    def get_balance(self):
        return self.user1.bal

    def withdraw(self, amount: float):
        if self.user1.bal >= amount:
            self.user1.bal -= amount
            return True
        return False

    def deposit(self,amount: float):
        self.user2.bal += amount

    def change_pin(self, new_pin: str):
        self.user1.pin = new_pin

class SelectLangPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()
        self.label = QLabel("Please Select Language / لطفا زبان را انتخاب کنید")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        hl = QHBoxLayout()

        english_button = QPushButton("English")
        english_button.clicked.connect(lambda: self.select_language('EN'))
        hl.addWidget(english_button)

        persian_button = QPushButton("فارسی")
        persian_button.clicked.connect(lambda: self.select_language('FA'))
        hl.addWidget(persian_button)

        layout.addLayout(hl)

        self.setLayout(layout)

    def select_language(self, lang_code):
        self.parent.language = lang_code
        self.parent.update_ui_texts()
        self.parent.set_current_index('EnterPinPage')


class EnterPinPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.attempts_left = 3

        layout = QVBoxLayout()

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.pin_input = QLineEdit()
        self.pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.pin_input)

        self.btn_enter = QPushButton()
        self.btn_enter.clicked.connect(self.check_pin)
        layout.addWidget(self.btn_enter)

        self.msg_label = QLabel()
        self.msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.msg_label)

        self.setLayout(layout)

    def update_texts(self):
        if self.parent.language == 'FA':
            self.label.setText("ورود رمز کارت")
            self.btn_enter.setText("ورود")
            self.pin_input.setPlaceholderText("رمز خود را وارد کنید")
            self.msg_label.setText("")
        else:
            self.label.setText("Enter PIN")
            self.btn_enter.setText("Enter")
            self.pin_input.setPlaceholderText("EnterPIN")
            self.msg_label.setText("")

    def check_pin(self):
        pin = self.pin_input.text()
        if self.parent.bank_db.validate_pass(pin):
            self.msg_label.setText("")
            self.attempts_left = 3
            self.pin_input.clear()
            self.parent.set_current_index('MainMenuPage')
        else:
            self.attempts_left -= 1
            if self.parent.language == 'FA':
                self.msg_label.setText(f"رمز اشتباه است. {self.attempts_left} تلاش باقی مانده")
            else:
                self.msg_label.setText(f"Incorrect PIN. {self.attempts_left} attempts left")
            self.pin_input.clear()
            if self.attempts_left == 0:
                QMessageBox.critical(self, "Error", "Too many wrong attempts. Exiting.")
                QApplication.quit()


class MainMenuPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        grid = QGridLayout()
        grid.setSpacing(60)

        self.balance_button = QPushButton()
        grid.addWidget(self.balance_button, 0, 0)

        self.withdraw_button = QPushButton()
        grid.addWidget(self.withdraw_button, 0, 7)

        self.transfer_button = QPushButton()
        grid.addWidget(self.transfer_button, 2, 0)
        self.change_pass_button = QPushButton()

        grid.addWidget(self.change_pass_button, 2, 7)
        self.exit_button = QPushButton()

        grid.addWidget(self.exit_button, 4, 0)


        self.balance_button.clicked.connect(lambda: self.parent.set_current_index('BalancePage'))
        self.withdraw_button.clicked.connect(lambda: self.parent.set_current_index('WithdrawPage'))
        self.transfer_button.clicked.connect(lambda: self.parent.set_current_index('TransferPage'))
        self.change_pass_button.clicked.connect(lambda: self.parent.set_current_index('ChangePinPage'))
        self.exit_button.clicked.connect(self.exit_atm)

        layout = QVBoxLayout()
        self.label = QLabel("Main Menu")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        layout.addLayout(grid)

        self.setLayout(layout)

    def update_texts(self):
        if self.parent.language == 'FA':
            self.label.setText("لطفا یک گزینه انتخاب کنید:")
            self.balance_button.setText("نمایش موجودی")
            self.withdraw_button.setText("برداشت وجه")
            self.transfer_button.setText("انتقال وجه")
            self.change_pass_button.setText("تغییر رمز عبور")
            self.exit_button.setText("خروج")
        else:
            self.label.setText("Please select an option:")
            self.balance_button.setText("View Balance")
            self.withdraw_button.setText("Withdraw Cash")
            self.transfer_button.setText("Transfer Funds")
            self.change_pass_button.setText("Change PIN")
            self.exit_button.setText("Exit")

    def exit_atm(self):
        QMessageBox.information(self, "Goodbye", "Thank you for using the ATM.")
        QApplication.quit()


class BalancePage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        layout = QVBoxLayout()
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.balance_label = QLabel()
        self.balance_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.balance_label)

        self.btn_ok = QPushButton()
        self.btn_ok.clicked.connect(lambda: self.parent.set_current_index('EndOperationPage'))
        layout.addWidget(self.btn_ok)

        self.setLayout(layout)

    def update_texts(self):
        if self.parent.language == 'FA':
            self.label.setText("موجودی حساب شما:")
            self.btn_ok.setText("ادامه")
        else:
            self.label.setText("Your account balance is:")
            self.btn_ok.setText("Continue")

    def show_balance(self):
        balance = self.parent.bank_db.get_balance()
        self.balance_label.setText(f"{balance:,.2f}")


class WithdrawPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        layout = QVBoxLayout()
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("")
        layout.addWidget(self.amount_input)

        self.btn_withdraw = QPushButton()
        layout.addWidget(self.btn_withdraw)

        self.msg_label = QLabel()
        self.msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.msg_label)
        self.btn_withdraw.clicked.connect(self.process_withdraw)
        self.setLayout(layout)

    def update_texts(self):
        if self.parent.language == 'FA':
            self.label.setText("مبلغ برداشت را وارد کنید:")
            self.amount_input.setPlaceholderText("مبلغ به تومان")
            self.btn_withdraw.setText("برداشت")
            self.msg_label.setText("")
        else:
            self.label.setText("Enter amount to withdraw:")
            self.amount_input.setPlaceholderText("Amount")
            self.btn_withdraw.setText("Withdraw")
            self.msg_label.setText("")

    def process_withdraw(self):
        text = self.amount_input.text()
        if text.replace('.', '', 1).isdigit():
            amount = float(text)
            if amount <= 0:
                if self.parent.language == 'FA':
                    self.msg_label.setText("لطفا مبلغ معتبر وارد کنید.")
                else:
                    self.msg_label.setText("Please enter a valid amount.")
        else:
            if self.parent.language == 'FA':
                self.msg_label.setText("لطفا مبلغ معتبر وارد کنید.")
            else:
                self.msg_label.setText("Please enter a valid amount.")

        success = self.parent.bank_db.withdraw(amount)
        if success:
            self.msg_label.setText("")
            self.amount_input.clear()
            self.parent.last_operation_message = (
                f"{'برداشت وجه موفق' if self.parent.language == 'FA' else 'Withdrawal successful'}: {amount:,.2f}"
            )
            self.parent.set_current_index('EndOperationPage')
        else:
            if self.parent.language == 'FA':
                self.msg_label.setText("موجودی کافی نیست.")
            else:
                self.msg_label.setText("Insufficient balance.")

class TransferPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        layout = QVBoxLayout()
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("")
        layout.addWidget(self.target_input)

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("")
        layout.addWidget(self.amount_input)

        self.btn_transfer = QPushButton()
        layout.addWidget(self.btn_transfer)

        self.msg_label = QLabel()
        self.msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.msg_label)

        self.btn_transfer.clicked.connect(self.process_transfer)

        self.setLayout(layout)

    def update_texts(self):
        if self.parent.language == 'FA':
            self.label.setText("شماره کارت مقصد را وارد کنید:")
            self.target_input.setPlaceholderText("شماره کارت مقصد")
            self.amount_input.setPlaceholderText("مبلغ به تومان")
            self.btn_transfer.setText("انتقال وجه")
            self.msg_label.setText("")
        else:
            self.label.setText("Enter target card number:")
            self.target_input.setPlaceholderText("Target card number")
            self.amount_input.setPlaceholderText("Amount")
            self.btn_transfer.setText("Transfer")
            self.msg_label.setText("")

    def process_transfer(self):
        target = self.target_input.text().strip()
        amount_text = self.amount_input.text()
        if target != self.parent.bank_db.user2.card:
            msg = "شماره کارت مقصد معتبر نیست." if self.parent.language == 'FA' else "Invalid target card number."
            self.msg_label.setText(msg)
            return
        if target == self.parent.bank_db.user1.card:
            msg = "نمیتوانید به همان کارت وجه منتقل کنید." if self.parent.language == 'FA' else "Cannot transfer to the same card."
            self.msg_label.setText(msg)
            return

        amount_text = amount_text.strip()
        if amount_text.replace('.', '', 1).isdigit():
            amount = float(amount_text)
            if amount <= 0:
                msg = "لطفا مبلغ معتبر وارد کنید." if self.parent.language == 'FA' else "Please enter a valid amount."
                self.msg_label.setText(msg)
        else:
            msg = "لطفا مبلغ معتبر وارد کنید." if self.parent.language == 'FA' else "Please enter a valid amount."
            self.msg_label.setText(msg)

        if self.parent.bank_db.withdraw(amount):
            self.parent.bank_db.deposit(amount)
            self.msg_label.setText("")
            self.target_input.clear()
            self.amount_input.clear()
            self.parent.last_operation_message = (
                f"{'انتقال وجه موفق' if self.parent.language == 'FA' else 'Transfer successful'}: {amount:,.2f}"
            )
            self.parent.set_current_index('EndOperationPage')
        else:
            msg = "موجودی کافی نیست." if self.parent.language == 'FA' else "Insufficient balance."
            self.msg_label.setText(msg)

class ChangePinPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        layout = QVBoxLayout()
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.old_pin_input = QLineEdit()
        self.old_pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.old_pin_input.setPlaceholderText("")

        self.old_pin_input.setPlaceholderText(
            "Enter old PIN" if self.parent.language != 'FA' else "رمز قبلی را وارد کنید")
        layout.addWidget(self.old_pin_input)

        self.new_pin_input = QLineEdit()
        self.new_pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_pin_input.setPlaceholderText(
            "Enter new PIN" if self.parent.language != 'FA' else "رمز جدید را وارد کنید")
        layout.addWidget(self.new_pin_input)

        self.confirm_pin_input = QLineEdit()
        self.confirm_pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_pin_input.setPlaceholderText(
            "Confirm new PIN" if self.parent.language != 'FA' else "تایید رمز جدید")
        layout.addWidget(self.confirm_pin_input)

        self.btn_change = QPushButton()
        self.btn_change.clicked.connect(self.change_pin)
        layout.addWidget(self.btn_change)

        self.msg_label = QLabel()
        self.msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.msg_label)

        self.setLayout(layout)

    def update_texts(self):
        if self.parent.language == 'FA':
            self.label.setText("تغییر رمز عبور")
            self.old_pin_input.setPlaceholderText("رمز قبلی را وارد کنید")
            self.new_pin_input.setPlaceholderText("رمز جدید را وارد کنید")
            self.confirm_pin_input.setPlaceholderText("تایید رمز جدید")
            self.btn_change.setText("ثبت تغییرات")
            self.msg_label.setText("")
        else:
            self.label.setText("Change PIN")
            self.old_pin_input.setPlaceholderText("Enter old PIN")
            self.new_pin_input.setPlaceholderText("Enter new PIN")
            self.confirm_pin_input.setPlaceholderText("Confirm new PIN")
            self.btn_change.setText("Submit")
            self.msg_label.setText("")

    def change_pin(self):
        old_pin = self.old_pin_input.text()
        new_pin = self.new_pin_input.text()
        confirm_pin = self.confirm_pin_input.text()

        if not self.parent.bank_db.validate_pass(old_pin):
            self.msg_label.setText(
                "رمز قبلی نادرست است." if self.parent.language == 'FA' else "Old PIN is incorrect.")
            return

        if len(new_pin) < 4 or not new_pin.isdigit():
            self.msg_label.setText(
                "رمز جدید باید حداقل 4 رقم و فقط عدد باشد." if self.parent.language == 'FA' else "New PIN must be at least 4 digits.")
            return

        if new_pin != confirm_pin:
            self.msg_label.setText(
                "رمز جدید و تایید آن مطابقت ندارند." if self.parent.language == 'FA' else "New PIN and confirmation do not match.")
            return

        self.parent.bank_db.change_pin(new_pin)
        self.msg_label.setText("")
        self.old_pin_input.clear()
        self.new_pin_input.clear()
        self.confirm_pin_input.clear()
        self.parent.last_operation_message = ("تغییر رمز موفقیت‌آمیز بود." if self.parent.language == 'FA' else "PIN change successful.")
        self.parent.set_current_index('EndOperationPage')

class EndOperationPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()
        self.msg_label = QLabel()
        self.msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.msg_label)

        self.btn_new_op = QPushButton()
        self.btn_exit = QPushButton()

        hl = QHBoxLayout()
        hl.addWidget(self.btn_new_op)
        hl.addWidget(self.btn_exit)

        layout.addLayout(hl)

        self.btn_new_op.clicked.connect(self.new_operation)
        self.btn_exit.clicked.connect(self.exit_atm)

        self.setLayout(layout)

    def update_texts(self):
        if self.parent.language == 'FA':
            self.btn_new_op.setText("عملیات جدید")
            self.btn_exit.setText("خروج")
            self.msg_label.setText(self.parent.last_operation_message or "عملیات با موفقیت انجام شد.")
        else:
            self.btn_new_op.setText("New Operation")
            self.btn_exit.setText("Exit")
            self.msg_label.setText(
            self.parent.last_operation_message or "Operation completed successfully.")

    def new_operation(self):
        self.parent.set_current_index('MainMenuPage')

    def exit_atm(self):
        QMessageBox.information(self, "Goodbye", "Thank you for using the ATM.")
        QApplication.quit()

class ATMApp(QStackedWidget):
    def __init__(self):
        super().__init__()

        self.language = 'EN'
        self.current_card = None
        self.last_operation_message = ""
        self.bank_db = Database()

        self.pages = {
            'LanguageSelectionPage': SelectLangPage(self),
            'EnterPinPage': EnterPinPage(self),
            'MainMenuPage': MainMenuPage(self),
            'BalancePage': BalancePage(self),
            'WithdrawPage': WithdrawPage(self),
            'TransferPage': TransferPage(self),
            'ChangePinPage': ChangePinPage(self),
            'EndOperationPage': EndOperationPage(self),
        }

        for page in self.pages.values():
            self.addWidget(page)

        self.setWindowTitle("ATM Simulator")

        self.set_current_index('LanguageSelectionPage')

    def set_current_index(self, page_name: str):
        page = self.pages.get(page_name)
        if page is None:
            return

        self.setCurrentWidget(page)

        if hasattr(page, "update_texts"):
            page.update_texts()

        if page_name == 'BalancePage' and hasattr(page, "show_balance"):
            page.show_balance()

        self.last_operation_message = "" if page_name != 'EndOperationPage' else self.last_operation_message

    def update_ui_texts(self):
        for page in self.pages.values():
            if hasattr(page, "update_texts"):
                page.update_texts()



app = QApplication(sys.argv)
window = ATMApp()
window.resize(400, 300)
window.setStyleSheet("background-image: url('C:/Users/AliMhd_Pr/OneDrive/Desktop/ap/ATM/ALibackground.jpg'); background-repeat: no-repeat; background-position: center;")


window.show()
sys.exit(app.exec())
