# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KwJOmo8HDsQ0PIdPe3_jV_537JEA3UPR
"""



import math
import pandas as pd 
import numpy as np 
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, LSTM 
import matplotlib.pyplot as plt 

plt.style.use('fivethirtyeight')

stockData = pd.read_csv('ACST.csv')
stockData

stockData.shape

plt.figure(figsize=(16,7))
plt.title('Closing price of A')
plt.plot(stockData['Close'])
plt.xlabel('Date')
plt.ylabel('Closing Price USD')
plt.show

data = stockData.filter(['Close'])
dataset = data.values
training_data_len = math.ceil(len(dataset) * .8)

scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(dataset)
scaled_data

train_data = scaled_data[0:training_data_len ,:]
trian_data = np.array(train_data)
x_train = []
y_train = []

for i in range(60, len(train_data)):
  x_train.append(train_data[i-60:i, 0])
  y_train.append(train_data[i, 0])
  if i<=61:
    print(x_train)
    print(y_train)
    print()

x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
x_train.shape

model = Sequential()
model.add(LSTM(50, return_sequences = True, input_shape = (x_train.shape[1], 1)))
model.add(LSTM(50, return_sequences = False))
model.add(Dense(25))
model.add(Dense(1))

model.compile(optimizer='adam', loss = 'mean_squared_error')

model.fit(x_train, y_train, batch_size = 1, epochs=1)

test_data = scaled_data[training_data_len - 60: , :]
x_test = []
y_test = dataset[training_data_len:, :]

for i in range(60, len(test_data)):
  x_test.append(train_data[i-60:i, 0])
x_test

x_test = np.array(x_test)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)