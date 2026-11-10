from dataHandler import decomposeDecription
from filesHandler import saveResults, getAliases, getData, setup_logger

log = setup_logger()

data = getData()
aliasesDictionary = getAliases()
for position in data:
    position["apple_variety"], position["apple_keyword"], position["apple_color"], position["apple_package"], position["apple_weight_KG"], errors = decomposeDecription(position['descr'], aliasesDictionary)
    for error in errors:
        log.warning("id=%s | reason=%r", position['prod_id'], error)


saveResults(data)