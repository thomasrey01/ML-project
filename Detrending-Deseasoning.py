import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv
import math
from scipy.optimize import curve_fit
import copy


df = pd.read_excel('financialdata.xlsx')
df_quarter = pd.read_excel('quarter_data.xlsx')
df_monthly = pd.read_excel('monthly.xlsx')

quarter_data = np.array(df_quarter)
monthly_data = np.array(df_monthly)

#Create a function to separate the time and the respective financial value
month = []
for i in range(len(monthly_data)):
  dummy = []
  dummy.append(monthly_data[i][0:6])
  dummy2 = []
  for j in (monthly_data[i][6:]):
    if math.isnan(j) == False:
      dummy2.append(j)
  month.append((dummy[0], dummy2))

def create_months(data):
  copy = data
  final = []
  for i in range(len(data)):
    initial_year = data[i][0][4]
    initial_month = data[i][0][5]
    dum = []
    dum2 = []
    for j in range(len(data[i][1])):
      dum.append((initial_year + round(((j + initial_month)/12) - 0.5), (initial_month + j%12) % 13 ))
    dum2.append(dum)
    dum2.append(copy[i][0])
    dum2.append(copy[i][1])
    final.append(dum2)
  return final


# Polynomial Detrending

def function(x, a, b):
 return a * x + b



def detrend_polynomial(data):
  copy2 = copy.deepcopy(data)
  copy1 = copy.deepcopy(copy2)
  for i in range(len(copy1)):

    x = np.arange(0, len(copy1[i][2]), 1)
    y = copy1[i][2]
    popt, _ = curve_fit(function, x, y)
    a, b = popt
    # print(a, b)
    for j in range(len(copy1[i][2])):
      # print(copy[i][2][j])
      copy1[i][2][j] = copy1[i][2][j] - function(x[j], a, b)
      # print(function(j, a, b))

  return copy1
  # plt.scatter(x, y)
  # plt.plot(function(x, a, b))


# Detrending using the difference of the previous value
def detrending_difference(data):
  final = []
  for i in range(len(data)):
    subs = []
    for j in range(len(data[i][2]) - 1):
      subs.append(data[i][2][j+1] - data[i][2][j])
    final.append( (data[i][0][1:], data[i][1], subs))
  return final


polynomial = detrend_polynomial(month_final)
plt.plot(polynomial[0][2])
plt.plot(month_final[0][2])


# Deseasoning
def month_deseasoning_difference(data):
  final = []
  for i in range(len(data)):
    subs = []
    for j in range(len(data[i][2]) - 12):
      subs.append(data[i][2][j] - data[i][2][j + 12])
    final.append((data[i][0][12:], data[i][1], subs))
  return final

plt.plot(month_deseasoning_difference(month_final)[0][2], label = "Deseason")
plt.plot(month_final[0][2], label = "Normal")
plt.legend()
plt.show
