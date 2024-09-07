import os
import tkinter as tk
from tkinter import messagebox
import requests

API_KEY = os.environ.get('API_KEY')
BASE_URL = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/'
CURRENCIES = ['GEL', 'USD', 'EUR', 'TRY', 'CNY', 'KRW']


class Converter(tk.Tk):
    """
    Main application class for the Currency Converter GUI.
    """
    def __init__(self):
        super().__init__()
        self.title('Currency Converter')
        self.setup_window()
        self.currency_frame = Currencies(self)
        self.conversion_frame = AmountToConvert(self)
        self.result_frame = Result(self)
        self.setup_widgets()

    def setup_window(self):
        """
        Configures the main window's size and position.
        Centers the window on the screen.
        """
        window_width, window_height = 600, 500
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_coordinate = (screen_width // 2) - (window_width // 2)
        y_coordinate = (screen_height // 2) - (window_height // 2)
        self.geometry(f'{window_width}x{window_height}+{x_coordinate}+{y_coordinate}')

    def setup_widgets(self):
        """
        Positions the main widgets of the application.
        Binds 'conversion' and 'clear' methods to the relevant buttons and keys.
        """
        for frame in (self.currency_frame, self.conversion_frame, self.result_frame):
            frame.pack(padx=20, pady=20)

        self.conversion_frame.convert_button.config(command=self.convert_currency)
        self.conversion_frame.entry.bind('<Return>', lambda event: self.convert_currency())
        self.result_frame.clear_button.config(command=self.clear)

    @staticmethod
    def get_conversion_rate(source_currency: str, target_currency: str) -> float:
        """
        Fetches the conversion rate from the API for the given currencies.

        :param source_currency: The currency to convert from.
        :param target_currency: The currency to convert to.
        :return: float: The conversion rate.
        :raises: Exception: If there's an error fetching the conversion rate.
        """
        url = f'{BASE_URL}{source_currency}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data['conversion_rates'][target_currency]
        except requests.RequestException as e:
            raise Exception(f'Error fetching conversion rate: {e}')

    def convert_currency(self):
        """
        Performs the currency conversion based on user's input.
        Handles input validation, currency conversion, and result display.
        Shows appropriate warning messages for invalid inputs.
        """
        try:
            source_currency = self.currency_frame.selected_currency_from.get()
            target_currency = self.currency_frame.selected_currency_to.get()
            amount = float(self.conversion_frame.entry.get())

            if amount == 0:
                messagebox.showwarning('Warning', 'Please enter an amount greater than zero.')
            elif target_currency == source_currency:
                messagebox.showwarning('Warning', 'Please select different currencies.')
                return

            rate = self.get_conversion_rate(source_currency, target_currency)
            converted_amount = round(amount * rate, 2)
            self.result_frame.conversion_result.config(
                text = f'You can buy {converted_amount} {target_currency} with {amount} {source_currency}')

        except ValueError:
            messagebox.showwarning('Warning', 'Please enter a valid amount.')
        except Exception as error:
            messagebox.showerror(f'Error: {error}')

    def clear(self):
        """
        Clears the amount input field and resets the result display.
        """
        self.conversion_frame.entry.delete(0, tk.END)
        self.result_frame.conversion_result.config(text='Conversion Result:')


class Currencies(tk.Frame):
    """
    Frame for selecting the source and target currencies.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.selected_currency_from = tk.StringVar(value='GEL')
        self.selected_currency_to = tk.StringVar(value='USD')
        self.from_frame = tk.LabelFrame(self, text='Currency to convert from:', font=('Courier', 12, 'bold'))
        self.to_frame = tk.LabelFrame(self, text='Currency to convert to:', font=('Courier', 12, 'bold'))
        self.from_menu = tk.OptionMenu(self.from_frame, self.selected_currency_from, *CURRENCIES)
        self.to_menu = tk.OptionMenu(self.to_frame, self.selected_currency_to, *CURRENCIES)
        for menu in (self.from_menu, self.to_menu):
            menu.config(font=('Courier', 12), background='#ffc5b7')
        self.position_widgets()

    def position_widgets(self):
        """
        Positions the currency selection dropdown menus and their labels.
        """
        for index, frame in enumerate([self.from_frame, self.to_frame]):
            frame.grid(row=0, column=index, padx=5, pady=30, sticky=tk.NSEW)
        for index, menu in enumerate([self.from_menu, self.to_menu]):
            menu.grid(row=0, column=index, padx=5, pady=12, sticky=tk.EW)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)


class AmountToConvert(tk.Frame):
    """
    Frame for entering the amount to convert and initiating conversion.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.label = tk.Label(
            self, text='Enter the amount to convert:', font=('Courier', 12, 'bold'), anchor='center'
        )
        self.label.pack(pady = 8)
        self.entry = tk.Entry(
            self, font=('Courier', 12), width=20, highlightcolor='#524c42', justify=tk.CENTER
        )
        self.entry.pack(pady = 8)
        self.convert_button = tk.Button(
            self, text='Convert', bg='Salmon', font=('Courier', 12, 'bold'), bd=3, width=12
        )
        self.convert_button.pack(pady=8)


class Result(tk.Frame):
    """
    Frame for displaying the conversion result and 'clear' button.
    """
    def __init__(self, parent):
        super().__init__(parent)

        self.conversion_result = tk.Label(
            self, text='Conversion Result:', font=('Courier', 12, 'bold'), anchor=tk.CENTER
        )
        self.conversion_result.pack(pady=7)
        self.clear_button = tk.Button(
            self, text='Clear', bg='Salmon', font=('Courier', 12, 'bold'), bd=3, width=12
        )
        self.clear_button.pack(pady=7)


def main():
    """
    Initialize and run the Currency Converter application.
    """
    app = Converter()
    app.mainloop()

if __name__ == '__main__':
    main()
