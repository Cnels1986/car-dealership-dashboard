import matplotlib.pyplot as plt, mpld3
from flask import Flask
from flask import render_template
import matplotlib
import numpy as np
import json
from re import sub
from decimal import Decimal
import math
import operator
#
# app = Flask(__name__)
#
# @app.route("/")
# def index():
#     return render_template('dashboard.html', profit=total_profit, tableData = sorted_chartData)

with open('sales_staff.json', 'r') as staffFile:
    staff = json.loads(staffFile.read())

with open('sales.json', 'r') as salesFile:
    sales = json.loads(salesFile.read())

personCount = 1
chartData = []

# loops through the data, counting the number of cars sold by a sales person then adds its price to a total
for person in staff:
    carsSold = 0
    salesAmount = 0
    for sale in sales:
        if(sale['salesperson'] == personCount):
            #converts the money string to a decimal datatype
            base_price = Decimal(sub(r'[^\d.]', '', sale['base_price']))
            accessories = Decimal(sub(r'[^\d.]', '', sale['accessories']))
            taxes = Decimal(sub(r'[^\d.]', '', sale['taxes']))

            carsSold += 1   #increments cars sold
            salesAmount += (base_price + accessories) - taxes   #adds the amount made after taxes
    commission = float(salesAmount) * person['commission']
    name = person['first_name'] + " " + person['last_name']
    dict = {'name': name, 'carsSold': carsSold, 'saleAmount': '${:,.2f}'.format(float(salesAmount)), 'commission': '${:,.2f}'.format(round(commission,2))}
    chartData.append(dict)
    personCount += 1

sorted_chartData = sorted(chartData, key=operator.itemgetter('carsSold'), reverse=True)
# print(sorted_chartData)
salesRankingSold = {}
salesRankingAmount = {}
salesRankingCommission = {}

for rank in sorted_chartData:
    names = rank['name']
    salesRankingSold[name] = rank['carsSold']
    salesRankingAmount[name] = rank['saleAmount']
    salesRankingCommission[name] = rank['commission']

names = list(salesRankingSold.keys())
valuesSold = list(salesRankingSold.values())
valuesAmount = list(salesRankingAmount.values())
valuesCommission = list(salesRankingCommission.values())
# print(names)
# print(valuesSold)
# print(valuesAmount)
# print(valuesCommission)


models = {}
makes = {}
# finds the total profit made from the dataset
total_profit = 0
for sale in sales:
    base_price = Decimal(sub(r'[^\d.]', '', sale['base_price']))
    accessories = Decimal(sub(r'[^\d.]', '', sale['accessories']))
    taxes = Decimal(sub(r'[^\d.]', '', sale['taxes']))
    total_profit += (base_price + accessories) - taxes

    model = sale['model']
    make = sale['make']

    # checks the dictionary containing makes, add entry if it doesn't exist or increments
    if(make in makes):
        makes[make] += 1
    else:
        makes[make] = 1

    # checks the dictionary containing the models, adds entry if it doesn't exist or increments
    if(model in models):
        models[model] += 1
    else:
        models[model] = 1

total_profit = '${:,.2f}'.format(total_profit)
# print(total_profit)
# creates sorted lists of the dictionaries, list contains tuples and is sorted by values
makesSorted = sorted(makes.items(), key=operator.itemgetter(1), reverse=True)
modelsSorted = sorted(models.items(), key=operator.itemgetter(1), reverse=True)
top10makes = makesSorted[0:10]
top10models = modelsSorted[0:10]

name = []
values = []
for model in top10models:
    name.append(model[0])
    values.append(model[1])
fig, axs = plt.subplots()
axs.bar(name, values)
axs.set_ylabel('Number Sold')
axs.set_xlabel('Models')
axs.set_title('Top 10 Models Sold')
plt.xticks(rotation=45)
fig.tight_layout()
# mpld3.show()
fig1 = mpld3.fig_to_html(fig)
print(fig1)

# name1 = []
# values1 = []
# for make in top10makes:
#     name1.append(make[0])
#     values1.append(make[1])
# fig, axs = plt.subplots()
# axs.bar(name, values)
# axs.set_ylabel('Number Sold')
# axs.set_xlabel('Makes')
# axs.set_title('Top 10 Makes Sold')
# plt.xticks(rotation=45)
# fig.tight_layout()
# mpld3.show()
