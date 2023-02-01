import pandas as pd
# import xlrd
import os
"""
pip install openpyxl
"""
cur_directory = os.curdir

df = pd.read_excel("/Users/wykeen/PycharmProjects/scrapeZalora/Data/Question 1 Dataset.xlsx", engine ='openpyxl')

for sku in df["sku"][:5]:
    print(sku)