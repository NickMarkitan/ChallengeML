import pandas as pd
from datetime import datetime
import csv

def getData ():
    """Загружает данные из файла с описаниями и возвращает в виде списка словарей"""
    with open("data/data/raw_desc.csv", newline="", encoding="utf-8") as dataFile:
        reader = csv.DictReader(dataFile, delimiter=",")
        return list(reader)

def getAliases():
    """Берёт набор сокращение сортов и возвращает ввиде словаря сокращение->полное название"""
    aliasesDF = pd.read_excel("data/data/apple_var.xlsx", header=0)
    return dict(zip(aliasesDF["name_var"], aliasesDF["name"]))

def saveResults(data):
    """Сохраняет полученные результаты в файл"""
    dataFrame = pd.DataFrame(data)
    timestamp = datetime.now().strftime("%y-%m-%d_%H-%M-%S")
    dataFrame.to_excel(f"result_{timestamp}.xlsx", index=False)