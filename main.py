from dataHandler import decomposeDecription
from filesHandler import saveResults, getAliases, getData

data = getData()
aliasesDictionary = getAliases()
for position in data:
    position["apple_variety"], position["apple_keyword"], position["apple_color"], position["apple_package"], position["apple_wtight_KG"] = decomposeDecription(position['descr'], aliasesDictionary)

saveResults(data)