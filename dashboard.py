import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import json
from re import sub
from decimal import Decimal

with open('sales_staff.json', 'r') as staffFile:
    staff = json.loads(staffFile.read())
    # print(staff)

with open('sales.json', 'r') as salesFile:
    sales = json.loads(salesFile.read())
    # print(sales)

personCount = 1

# for person in staff:
#     carsSold = 0
#     salesAmount = 0
#     for sale in sales:
#         if(sale['salesperson'] == personCount):
#             carsSold += 1
#             salesAmount +=
#     print(carsSold)
#


# finds the total profit made from the dataset
total_profit = 0
for sale in sales:
    base_price = Decimal(sub(r'[^\d.]', '', sale['base_price']))
    accessories = Decimal(sub(r'[^\d.]', '', sale['accessories']))
    taxes = Decimal(sub(r'[^\d.]', '', sale['taxes']))
    total_profit += (base_price + accessories) - taxes
print('${:,.2f}'.format(total_profit))
