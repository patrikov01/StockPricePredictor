**Stock Price Predictor**
Introduction
The Stock Price Predictor is a tool that predicts the future price of a particular stock using historical data and machine learning algorithms. The user can use either Support Vector Regression (SVR) or Linear Regression algorithms to predict the future price. The tool is built using Tkinter for GUI, Pandas for data pre-processing, Numpy for numerical calculations, Scikit-learn for machine learning and Matplotlib for visualizing the results.

Requirements
Before running the Stock Price Predictor, make sure you have the following packages installed:

Tkinter
Pandas
Numpy
Scikit-learn
Matplotlib
You can install these packages by running the following command in your terminal/command prompt:

pip install tkinter pandas numpy scikit-learn matplotlib
Usage

Run the Stock Price Predictor by executing the following command in your terminal/command prompt:
python main.py
A GUI will appear, where you can select the stock data file you want to use for prediction. The data file should be in .csv format and should have the following columns:
Date
Open
High
Low
Close
Adj Close
Volume
To select the data file, click on the "Open" button and select the desired file.

Finally, click on the "Predict" button to get the predicted stock prices. The results will be displayed in a graph, where the blue line represents the actual stock prices and the orange and the green lines represent the predicted stock prices.

Conclusion
The Stock Price Predictor is a simple yet powerful tool that can help you predict the future price of a stock based on its historical data. It's a great tool for stock market enthusiasts and investors who want to make informed decisions. However, it's important to note that the predictions are not 100% accurate and should be used as a reference only. The stock market is inherently unpredictable, and there can be many factors that can affect the stock prices.
