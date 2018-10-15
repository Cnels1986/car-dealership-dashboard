import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import json
from re import sub
from decimal import Decimal
import math
import operator

with open('sales_staff.json', 'r') as staffFile:
    staff = json.loads(staffFile.read())
    # print(staff)

with open('sales.json', 'r') as salesFile:
    sales = json.loads(salesFile.read())
    # print(sales)

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
    dict = {'first': person['first_name'], 'last': person['last_name'], 'carsSold': carsSold, 'saleAmount': float(salesAmount), 'commission': round(commission,2)}
    chartData.append(dict)
    personCount += 1

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

makesSorted = sorted(makes.items(), key=operator.itemgetter(1), reverse=True)
modelsSorted = sorted(models.items(), key=operator.itemgetter(1), reverse=True)
top10models = modelsSorted[0:10]
