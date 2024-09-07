import sys
import os
import requests
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox
from PyQt5.QtCore import Qt
from PyQt5 import uic

# Constants
USERNAME = 'admin'
PASSWORD = 'admin'
API_KEY = os.environ.get('API_KEY') # API Key from environment variables
BASE_URL = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/' # Base URL for currency conversion API
CURRENCIES = ['GEL', 'USD', 'EUR', 'TRY', 'CNY', 'KRW'] # List of available currencies


class MainWindow(QMainWindow):
    """
    Main window class that manages the login page and converter page using stacked widgets.
    It initializes the login and converter pages, and manages key events on both pages.
    """
    def __init__(self):
        super(MainWindow, self).__init__()

        # Load the UI file
        try:
            uic.loadUi('application_design.ui', self)
        except Exception as error:
            print(f'Error loading UI file: {error}')
            sys.exit(1)

        # Instantiate the LoginPage and ConverterPage
        self.login_page = LoginPage(self)
        self.converter_page = ConverterPage(self)

        # Set initial page to the login page
        self.stackedWidget.setCurrentWidget(self.loginPage)

    def keyPressEvent(self, event):
        """
        Handles key press events for both the login and converter pages.
        If Enter/Return is pressed on the login page, it triggers the login.
        If Enter/Return is pressed on the converter page, it triggers the currency conversion.
        """
        # Get the current active page
        current_widget = self.stackedWidget.currentWidget()

        if current_widget == self.loginPage:
            if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
                self.login_page.login_on_click()

        elif current_widget == self.converterPage:
            if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
                self.converter_page.convert_currency()


class LoginPage:
    """
    Class responsible for handling the login page functionality.
    It validates the username and password, and switches to the converter page upon successful login.
    """
    def __init__(self, main_window):
        self.main_window = main_window # Reference to the MainWindow instance

        # Find UI elements related to log in functionality
        self.login_label = self.main_window.findChild(QLabel, 'loginLabel')
        self.username_input = self.main_window.findChild(QLineEdit, 'usernameInput')
        self.password_input = self.main_window.findChild(QLineEdit, 'passwordInput')
        self.login_button = self.main_window.findChild(QPushButton, 'loginButton')

        # Connect login button to the login function
        self.login_button.clicked.connect(self.login_on_click)

        # Set focus on the username input field
        self.username_input.setFocus()

    def login_on_click(self):
        """
        Handles the login button click event.
        Validates the username and password, and switches to the converter page if correct.
        Shows appropriate warning message for invalid inputs.
        """
        username = self.username_input.text()
        password = self.password_input.text()
        if username == USERNAME and password == PASSWORD:
            self.main_window.stackedWidget.setCurrentWidget(self.main_window.converterPage)
            self.reset_fields()
        else:
            QMessageBox.critical(self.main_window, 'Currency Converter Login', 'Incorrect username or password!')

    def reset_fields(self):
        """
        Resets the login input fields and sets focus on the username input field.
        """
        self.username_input.clear()
        self.password_input.clear()
        self.username_input.setFocus()


class ConverterPage:
    def __init__(self, main_window):
        self.main_window = main_window # Reference to the MainWindow instance

        # Find UI elements related to currency conversion functionality
        self.currency_from_label = self.main_window.findChild(QLabel, 'currencyFromLabel')
        self.currency_to_label = self.main_window.findChild(QLabel, 'currencyToLabel')
        self.currency_from_menu = self.main_window.findChild(QComboBox, 'currencyFromComboBox')
        self.currency_to_menu = self.main_window.findChild(QComboBox, 'currencyToComboBox')
        self.conversion_amount_input = self.main_window.findChild(QLineEdit, 'amountInput')
        self.convert_button = self.main_window.findChild(QPushButton, 'convertButton')
        self.conversion_result_label = self.main_window.findChild(QLabel, 'resultLabel')
        self.clear_button = self.main_window.findChild(QPushButton, 'clearButton')
        self.logout_button = self.main_window.findChild(QPushButton, 'logoutButton')

        # Connect the currency menu signals and buttons
        self.currency_from_menu.currentIndexChanged.connect(self.update_currency_to_menu)
        self.currency_to_menu.currentIndexChanged.connect(self.update_currency_from_menu)
        self.logout_button.clicked.connect(self.logout_on_click)
        self.convert_button.clicked.connect(self.convert_currency)
        self.clear_button.clicked.connect(self.clear_on_click)

    def update_currency_to_menu(self):
        """
        Updates the target currency menu when a new option is selected in the source currency menu.
        """
        self.update_menu_options(self.currency_from_menu, self.currency_to_menu)

    def update_currency_from_menu(self):
        """
        Updates the source currency menu when a new option is selected in the target currency menu.
        """
        self.update_menu_options(self.currency_to_menu, self.currency_from_menu)

    @staticmethod
    def update_menu_options(source_currency_menu: QComboBox, target_currency_menu: QComboBox):
        """
        Disables the currently selected option in the opposite currency menu
        to prevent the user from selecting the same currency for conversion.
        :param source_currency_menu: The source currency menu.
        :param target_currency_menu: The target currency menu.
        """
        currency_selected = source_currency_menu.currentText()

        # Enable all items in the target currency menu
        for i in range(target_currency_menu.count()):
            target_currency_menu.model().item(i).setEnabled(True)

        # Disable the currently selected item in the source currency menu
        matching_index = target_currency_menu.findText(currency_selected)
        if matching_index >= 0:
            target_currency_menu.model().item(matching_index).setEnabled(False)

        # Ensure the target currency menu does not have the same selected currency
        if target_currency_menu.currentText() == currency_selected:
            for i in range(target_currency_menu.count()):
                if target_currency_menu.model().item(i).isEnabled():
                    target_currency_menu.setCurrentIndex(i)
                    break

    @staticmethod
    def get_conversion_rate(source_currency: str, target_currency: str) -> float:
        """
        Fetches the conversion rate from the API for the given currencies.
        :param source_currency: The currency to convert from.
        :param target_currency: The currency to convert to.
        :return: The conversion rate.
        """
        url = f'{BASE_URL}{source_currency}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data['conversion_rates'][target_currency]
        except requests.RequestException as error:
            raise Exception(f'Error fetching conversion rate: {error}')

    def convert_currency(self):
        """
        Performs the currency conversion based on user's input.
        Handles input validation, currency conversion, and result display.
        Shows appropriate warning messages for invalid inputs.
        """
        try:
            amount_to_convert = float(self.conversion_amount_input.text())
            if amount_to_convert <= 0:
                QMessageBox.warning(self.main_window, 'Warning', 'Please enter an amount greater than zero.')
                return

            # Get the selected currencies
            source_currency = self.currency_from_menu.currentText()
            target_currency = self.currency_to_menu.currentText()

            # Get the conversion rate and calculate the converted amount
            rate = self.get_conversion_rate(source_currency, target_currency)
            converted_amount = round(amount_to_convert * rate, 2)

            # Display the conversion result
            self.conversion_result_label.setText(
                f'{amount_to_convert} {source_currency} is equal to {converted_amount} {target_currency}'
            )
        except ValueError:
            QMessageBox.warning(self.main_window, 'Warning', 'Please enter a valid amount.')
        except Exception as error:
            QMessageBox.warning(self.main_window, 'Warning', f'{error}')

    def clear_on_click(self):
        """
        Clears the input fields and resets the currency menus to their default values.
        """
        self.conversion_amount_input.clear()
        self.conversion_result_label.setText('Conversion Result:')
        self.currency_from_menu.setCurrentIndex(0)
        self.currency_to_menu.setCurrentIndex(0)

    def logout_on_click(self):
        """
        Handles the logout button click event.
        Resets the fields on converter page, and switches back to the login page.
        """
        self.clear_on_click()
        self.main_window.stackedWidget.setCurrentWidget(self.main_window.loginPage)


def main():
    """
    Main function to run the PyQt application.
    """
    # Enable high DPI scaling for better UI rendering on high-resolution screens
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle('Currency Converter Application')
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
