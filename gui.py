import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import numpy as np
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import requests
import pandas_datareader as pdr
from sklearn.model_selection import train_test_split
import datetime

class StockPredictorApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.title("Stock Predictor")

        self.file_path = ""
        self.result_text = tk.StringVar()
        self.result_text.set("Enter a URL or select a file")

        self.url_label = tk.Label(self, text="URL")
        self.url_label.grid(row=0, column=0, padx=10, pady=10)

        self.url_entry = tk.Entry(self)
        self.url_entry.grid(row=0, column=1, padx=10, pady=10)
        
        self.file_label = tk.Label(self, text="File")
        self.file_label.grid(row=1, column=0, padx=10, pady=10)

        self.file_entry = tk.Entry(self)
        self.file_entry.grid(row=1, column=1, padx=10, pady=10)

        self.browse_button = tk.Button(self, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=1, column=2, padx=10, pady=10)

        self.predict_button = tk.Button(self, text="Predict", command=self.predict)
        self.predict_button.grid(row=2, column=0, padx=10, pady=10)

        self.exit_button = tk.Button(self, text="Exit", command=self.exit)
        self.exit_button.grid(row=2, column=2, padx=10, pady=10)

        self.result_label = tk.Label(self, textvariable=self.result_text)
        self.result_label.grid(row=3, column=0, padx=10, pady=10, columnspan=3)

        
    def fetch(self):
        url = self.url_entry.get()
        response = requests.get(url)
        self.data = response.json()

    def browse_file(self):
        self.file_path = filedialog.askopenfilename(initialdir = "/", title = "Select file", filetypes = (("CSV files", "*.csv"), ("all files", "*.*")))
        self.file_entry.config(state='normal')
        self.file_entry.delete(0, 'end')
        self.file_entry.insert(0, self.file_path)
        self.file_entry.config(state='readonly')
    
    def exit(self):
        self.exit_flag = True
        self.quit()
    
    def predict(self):
        while True:
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
                continue

        # Prepare the data for prediction
            X = np.array(range(0, len(stock_data))).reshape(-1, 1)
            y = stock_data["Close"].values

        # Train the SVM model
            svm = SVR(kernel="linear", C=1, epsilon=0.1)
            svm.fit(X, y)

        # Train the Linear Regression model
            linear_regression = LinearRegression()
            linear_regression.fit(X, y)

        # Use the models to make a prediction
            svm_prediction = svm.predict([[len(stock_data)]])[0]
            linear_regression_prediction = linear_regression.predict([[len(stock_data)]])[0]

        # Display the result in the GUI
            self.result_text.set(f"SVM: {svm_prediction}, Linear Regression: {linear_regression_prediction}")

            plt.plot(stock_data['Close'], label='Actual')
            plt.plot(svm_prediction, label='SVM Prediction')
            plt.plot(linear_regression_prediction, label='Linear Regression Prediction')
            plt.legend()
           
            
           # data = pd.read_csv(file_path)
           # dates = data['Date'].tolist()
           # close_prices = data['Close'].tolist()
            
           # ax=plt.subplot()
           # ax.plot(dates, close_prices)
           # ax.set_title("Stock Price over time")
           # plt.xticks(rotation=45)
           # plt.tight_layout()
            plt.show()
            
            self.file_entry.delete(0, tk.END)
            
            if self.exit_flag:
                break

if __name__ == "__main__":
    app = StockPredictorApp()
    app.mainloop()