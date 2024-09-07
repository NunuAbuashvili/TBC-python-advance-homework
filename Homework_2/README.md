# Currency Converter Application #

## Overview ##
This Currency Converter is a PyQt5-based desktop application that features a login system, 
and after successful login, allows users to convert between different currencies.

## Features ##
- Secure login system.
- Currency conversion between multiple currencies (GEL, USD, EUR, TRY, CNY, KRW).
- Real-time exchange rates fetched from an API.
- User-friendly GUI created with Qt Designer.
- Input validation and error handling.

## Requirements ##
- Python 3.6+
- PyQt5
- `requests` library

## Usage ##
Run the application.<br/>
Log in using the following credentials:
  - **Username**: admin
  - **Password**: admin

*On the converter page*:
- Select the source currency from the "From" dropdown.
- Select the target currency from the "To" dropdown.
- Enter the amount you want to convert.
- Click "Convert" to see the result.
- Use "Clear" to reset the form. 
- Click "Logout" to return to the login page.

*Restrictions*:
- You cannot convert between the same currencies.
- You cannot enter a non-numeric value as the amount to convert.
- You cannot leave the amount field blank or enter 0 as the amount.


## Project Structure ##
- `main.py`: The main application file.
- `application_design.ui`: Qt Designer UI file.
- `requirements.txt`: This file lists all the Python dependencies required for the project. It can be used to install all necessary libraries.
- `README.md`: Project description.

## Acknowledgments ##
Exchange rates provided by `ExchangeRate-API`.<br/>
GUI framework created by `PyQt5`.