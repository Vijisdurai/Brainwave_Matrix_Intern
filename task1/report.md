# ATM Interface Using Python

## Overview
This project is a fully functional ATM interface developed using Python and tkinter. The system allows users to log in using a secure PIN-based authentication, check their balance, deposit and withdraw funds, and view transaction history. The application provides a modern, user-friendly graphical interface for easy interaction.

## Objective
To develop a modern ATM interface with the following features:
- Secure user authentication
- Bank branding and personalized account display
- Core banking operations: balance check, deposit, withdrawal, and transaction history
- User-friendly GUI with enhanced usability

## Features
- **User Authentication**: Secure login with PIN-based authentication.
- **Account Information**: Displays the account holder's name and account number upon login.
- **Bank Branding**: Display of bank name ("Bank of Python") and logo.
- **Core Functionalities**: Check balance, deposit funds, withdraw funds, and view transaction history.
- **User-Friendly Interface**: Clean and modern layout with enlarged, color-coded buttons.
- **Error Handling**: Input validation and error messages for invalid actions or insufficient funds.
- **Debugging Support**: Integrated print statements to trace the execution flow and help with debugging.

## Libraries Used
- **tkinter**: For GUI development.
- **PIL (Pillow)**: For handling and displaying images.
- **messagebox** and **simpledialog**: For user input, feedback, and error messages.

## Execution Flow
1. **Startup**: The program starts with a welcome screen and displays the bank's logo.
2. **Login**: User enters their PIN to access their account.
3. **Main Menu**: Displays options such as check balance, deposit, withdraw, and view transaction history.
4. **Operations**: The selected operation is executed with appropriate success or error feedback.
5. **Logout**: The session ends, and the application closes.

## Conclusion
The ATM Interface project provides essential banking operations with a modern, easy-to-use GUI. It also includes debugging features to assist in development and troubleshooting.

## Installation

1. Clone or download the repository.
2. Install the required libraries:
   ```bash
   pip install tkinter pillow
