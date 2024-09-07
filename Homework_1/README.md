# Currency Converter GUI #

## Description ## 
This is a Currency Converter GUI Python application, built using Tkinter. It allows users to choose between different currencies and perform conversion using real-time exchange rates fetched from an API.

## Features ##
- Convert between multiple currencies (GEL, USD, EUR, TRY, CNY, KRW).
- Real-time exchange rates from ExchangeRate-API.
- Simple and user-friendly graphical interface.
- Input validation and error handling.

## Requirements ##

- Python 3.6+
- Tkinter (usually comes pre-installed with Python)
- Requests library

## Usage ##
1. Run the script.
2. Select the source and target currencies from the dropdown menus.
3. Enter the amount you want to convert.
4. Click the "Convert" button or press Enter to see the result.
5. Use the "Clear" button to reset the input and result.

#### _Restrictions:_ ####
- You cannot convert between the same currencies.
- You cannot enter a non-numeric value as the amount to convert.
- You cannot leave the amount field blank or enter 0 as the amount.

## Code Structure ##

- `Converter`: Main application class.
- `Currencies`: Frame for currency selection.
- `AmountToConvert`: Frame for amount input and conversion button.
- `Result`: Frame for displaying conversion result and clear button.

## Future Improvements ##
Currently, this application supports conversion between six currencies. In the future, I plan to add a feature that allows users to enter any currency they wish to convert to or from directly within the options' menu. Additionally, to minimize API calls due to the limitations of the free version, I aim to implement time-based caching. I am also considering developing a more advanced UI with additional features.

## Acknowledgments ##
Exchange rates provided by `ExchangeRate-API`.