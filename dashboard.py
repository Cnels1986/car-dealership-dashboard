import matplotlib.pyplot as plt, mpld3
from flask import Flask
from flask import render_template
import matplotlib, json, math, operator
import numpy as np
from re import sub
from decimal import Decimal

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('dashboard.html', profit=total_profit, tableData = sorted_chartData, fig1=fig1, fig2=fig2, name=name, name1=name1)

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
fig1, axs = plt.subplots()
axs.bar(name, values)
axs.set_ylabel('Number Sold')
axs.set_title('Top 10 Models Sold')
plt.xticks([])
fig1.tight_layout()
fig1 = json.dumps(mpld3.fig_to_dict(fig1))

name1 = []
values1 = []
for make in top10makes:
    name1.append(make[0])
    values1.append(make[1])
fig2, axs = plt.subplots()
axs.bar(name1, values1)
axs.set_ylabel('Number Sold')
axs.set_title('Top 10 Makes Sold')
plt.xticks([])
fig2.tight_layout()
fig2 = json.dumps(mpld3.fig_to_dict(fig2))
