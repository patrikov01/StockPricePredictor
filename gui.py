import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import numpy as np
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import requests

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

    def fetch_data_with_api_key(symbol, api_key):
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={api_key}"
        response = requests.get(url)
    
        if response.status_code == 200:
            data = response.json()
            time_series = data["Time Series (Daily)"]
            stock_data = []
            for date, values in time_series.items():
                stock_data.append({
                 "date": date,
                 "open": float(values["1. open"]),
                 "high": float(values["2. high"]),
                 "low": float(values["3. low"]),
                 "close": float(values["4. close"]),
                 "volume": int(values["5. volume"])
            })
            df = pd.DataFrame(stock_data)
            df["date"] = pd.to_datetime(df["date"])
            df.set_index("date", inplace=True)
            return df
        else:
         print("Failed to fetch data with the given API key")
         return None

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
            symbol = self.symbol_entry.get()
            api_key = self.api_key_entry.get()
        
            if file_path == "" and symbol == "":
             messagebox.showerror("Error", "Please select a file or enter a symbol")
             return
            elif file_path != "":
            # Load the stock data from a local file
             try:
                stock_data = pd.read_csv(file_path)
             except FileNotFoundError:
                messagebox.showerror("Error", "File not found")
                self.file_entry.delete(0, tk.END)
                continue
            if symbol != "":
             API_KEY = "78509L5D6INZ29LP"
             url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={API_KEY}"
             response = requests.get(url)
             data = response.json()
             if "Error Message" in data:
                 messagebox.showerror("Error", data["Error Message"])
                 return
            stock_data = pd.DataFrame(data["Time Series (Daily)"]).T
            stock_data.index = pd.to_datetime(stock_data.index)
            stock_data.sort_index(ascending=True, inplace=True)

        # Prepare the data for prediction
            x = np.array(range(0, len(stock_data))).reshape(-1, 1) 
            y = stock_data["Close"].values

        # Train the SVM model
            svm = SVR(kernel="linear", C=1, epsilon=0.1)
            svm.fit(x, y)

        # Train the Linear Regression model
            linear_regression = LinearRegression()
            linear_regression.fit(x, y)

        # Use the models to make a prediction
            svm_prediction = svm.predict([[len(stock_data)]])[0]
            linear_regression_prediction = linear_regression.predict([[len(stock_data)]])[0]

        # Display the result in the GUI
            self.result_text.set(f"SVM: {svm_prediction}, Linear Regression: {linear_regression_prediction}")
            
            plt.plot()
            plt.plot(stock_data['Close'], label='Actual')
            plt.legend()
            
            ax = plt.subplot()
            ax.plot(len(stock_data)+1, svm_prediction, 'ro', label='SVM Prediction')
            ax.plot(len(stock_data)+1, linear_regression_prediction, 'go', label='Linear Regression Prediction')
            ax.legend()  
            
            plt.show()
            
            self.file_entry.delete(0, tk.END)
            
            if self.exit_flag:
                break

if __name__ == "__main__":
    app = StockPredictorApp()
    app.mainloop()