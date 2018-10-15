import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import json

with open('sales_staff.json', 'r') as staffFile:
    staff = json.loads(staffFile.read())
    # print(staff)

with open('sales.json', 'r') as salesFile:
    sales = json.loads(salesFile.read())
    # print(sales)

for sale in sales:
    print(sale)
    print("--------")
