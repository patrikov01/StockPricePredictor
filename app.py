import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import numpy as np
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

class StockPredictorApp(tk.Tk):
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

        self.predict_button = tk.Button(self, text="Predict", command=self.predict)
        self.predict_button.grid(row=2, column=0, padx=10, pady=10)

        self.exit_button = tk.Button(self, text="Exit", command=self.exit)
        self.exit_button.grid(row=2, column=2, padx=10, pady=10)

        self.result_label = tk.Label(self, textvariable=self.result_text)
        self.result_label.grid(row=3, column=0, padx=10, pady=10, columnspan=3)
        
        self.symbol= tk.StringVar()
        
    def about(self):
        messagebox.showinfo("About", "This is a stock prediction Python project. It uses SVM and Linear Regression to predict stock prices. \n Georgi Patrikov 2023 ©")
        
    def open_file(self):
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
            x = np.array(range(0, len(stock_data))).reshape(-1, 1)
            y = stock_data["Close"].values

        # Train the SVM model
            svm = SVR(kernel="rbf", C=1, epsilon=0.1)
            svm.fit(x, y)

        # Train the Linear Regression model
            linear_regression = LinearRegression()
            linear_regression.fit(x, y)

        # Use the models to make a prediction
            svm_predictions = []
            linear_regression_predictions = []
            for i in range(len(stock_data), len(stock_data) + 21):
                svm_prediction = svm.predict([[i]])[0]
                linear_regression_prediction = linear_regression.predict([[i]])[0]
                svm_predictions.append(svm_prediction)
                linear_regression_predictions.append(linear_regression_prediction)
        
            self.result_text.set(f"SVM: {svm_predictions[-1]}, Linear Regression: {linear_regression_predictions[-1]}")
            
            # Plot the data and predictions
            plt.plot()
            plt.plot(stock_data['Close'], label='Actual')
            plt.legend()
            
            ax = plt.subplot()
            ax.plot(range(len(stock_data), len(stock_data)+21), svm_predictions, 'r', label='SVM Prediction')
            ax.plot(range(len(stock_data), len(stock_data)+21), linear_regression_predictions, 'g', label='Linear Regression Prediction')
            ax.legend()
            plt.show()
            
            self.file_entry.delete(0, tk.END)
                
            if self.exit_flag:
                break
