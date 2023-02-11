"""
Tkinter is used for creating graphical user interfaces (GUIs) in Python.
"""
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import numpy as np
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


class StockPredictorApp(tk.Tk):
    """This is a GUI application for stock price prediction.

    This class creates a Tkinter GUI for a stock price prediction program.
    The user can choose a stock price data file, select a prediction model,
    and view the predicted stock price.
    """

    def __init__(self):
        tk.Tk.__init__(self)

        self.title("Stock Predictor")

        self.file_path = ""
        self.result_text = tk.StringVar()
        self.result_text.set("Choose a button or select a file")

        about_button = tk.Button(self, text="About", command=self.about)
        about_button.grid(row=2, column=1, padx=10, pady=10)

        self.file_label = tk.Label(self, text="File")
        self.file_label.grid(row=1, column=0, padx=10, pady=10)

        self.file_entry = tk.Entry(self)
        self.file_entry.grid(row=1, column=1, padx=10, pady=10)

        self.open_button = tk.Button(self, text="Open", command=self.open_file)
        self.open_button.grid(row=1, column=2, padx=10, pady=10)

        self.predict_button = tk.Button(
            self, text="Predict", command=self.predict)
        self.predict_button.grid(row=2, column=0, padx=10, pady=10)

        self.exit_button = tk.Button(self, text="Exit", command=self.exit)
        self.exit_button.grid(row=2, column=2, padx=10, pady=10)

        self.result_label = tk.Label(self, textvariable=self.result_text)
        self.result_label.grid(row=3, column=0, padx=10, pady=10, columnspan=3)

    def about(self):
        """Show information about the Stock Price Predictor application. """
        message = "This is a stock prediction Python project. It uses SVM and Linear Regression"
        message += " to predict stock prices. \nGeorgi Patrikov 2023 ©"
        messagebox.showinfo("About", message)

    def open_file(self):
        """Open a file and display its path in the file entry widget."""
        self.file_path = filedialog.askopenfilename(
            initialdir="/",
            title="Select file",
            filetypes=(("CSV files", "*.csv"), ("all files", "*.*"))
        )
        self.file_entry.config(state='normal')
        self.file_entry.delete(0, 'end')
        self.file_entry.insert(0, self.file_path)
        self.file_entry.config(state='readonly')

    def exit(self):
        """Exit the programme """
        self.quit()

    def predict(self):
        """ 
        Predict stock prices using SVM and Linear Regression.
        This method first checks if the required file path has been set and the file exists. 
        If both of these conditions are met, the data from the file is loaded and preprocessed.
        Next, the stock prices are predicted using both SVM and Linear Regression.
        The predicted results are then displayed to the user in the form of a graph.
        """
        file_path = self.file_entry.get()

        if file_path == "":
            messagebox.showerror("Error", "Please select a file")
            return
    # Load the stock data using pandas
        try:
            stock_data = pd.read_csv(file_path)
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found")
            self.file_entry.delete(0, tk.END)

    # Prepare the data for prediction
        x_axis = np.array(range(0, len(stock_data))).reshape(-1, 1)
        y_axis = stock_data["Close"].values

    # Train the SVM model
        svm = SVR(kernel="rbf", C=1, epsilon=0.1)
        svm.fit(x_axis, y_axis)

    # Train the Linear Regression model
        linear_regression = LinearRegression()
        linear_regression.fit(x_axis, y_axis)

    # Use the models to make a prediction
        svm_predictions = []
        linear_regression_predictions = []
        for i in range(len(stock_data), len(stock_data) + 21):
            svm_prediction = svm.predict([[i]])[0]
            linear_regression_prediction = linear_regression.predict([[i]])[0]
            svm_predictions.append(svm_prediction)
            linear_regression_predictions.append(
                linear_regression_prediction)

        self.result_text.set(
            f"SVM: {svm_predictions[-1]},Linear Regression: {linear_regression_predictions[-1]}"
        )

        # Plot the data and predictions
        plt.plot()
        plt.plot(stock_data['Close'], label='Actual')
        plt.legend()

        ax_subplot = plt.subplot()
        ax_subplot.plot(range(len(stock_data), len(stock_data)+21),
                        svm_predictions, 'r', label='SVM Prediction')
        ax_subplot.plot(
            range(len(stock_data), len(stock_data)+21),
            linear_regression_predictions,
            'g',
            label='Linear Regression Prediction'
        )
        ax_subplot.legend()
        plt.show()

        self.file_entry.delete(0, tk.END)
