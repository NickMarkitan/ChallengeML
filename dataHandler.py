import re
from datetime import datetime

def decomposeDecription(strInput, varAliasesDict):
    """Возвращает набор параметров взятых из введённой строки"""
    strInput = strInput.lower()
    errors = []
    weight, wMessage = figureWeight(strInput)
    if wMessage != "":
        errors.append(wMessage)
    return findAliases(strInput, varAliasesDict), confirmIsApple(strInput), checkColor(strInput), checkPackageType(strInput), weight, errors

def findAliases(strInput, varAliasesDict):
    """Ищет в строке участки совпадающие с ключами передаваемого словаря и возвращает соответствующее значение словаря (первое совпадение)
    Предполагается для использования со словарём Алиас -> Полное название сорта"""
    key = next((key for key in varAliasesDict
        if re.search(rf"\b{re.escape(str(key))}\b", strInput)), None)
    return varAliasesDict[key] if key is not None else None

def confirmIsApple(strInput):
    """Ищет в строке участки похожие на упоминание яблок и возвращает 'Яблоки' если находит что-то подходящее"""
    return "Яблоки" if re.search(r"\bяблок", strInput, flags=re.IGNORECASE) else None

FALSE_FRIENDS_RE = re.compile(r"\bкраснодар\w*|\bкраснояр\w*|\bкраснод\w*")

colors = {
        "зелен": "Зеленый",
        "красн": "Красный",
        "желт": "Желтый",
    }

def checkColor(strInput):
    """Ищет в строке участки похожие на упоминание цвета яблок и возвращает универсальное полное слово первого найденого цвета"""
    strInput = strInput.lower().replace("ё", "е")
    text = FALSE_FRIENDS_RE.sub(" ", strInput)
    best = None

    for stem, color in colors.items():
        m = re.search(rf"\b{stem}", text)
        if m and (best is None or m.start() < best[0]):
            best = (m.start(), color)
    return best[1] if best else None

def checkPackageType(strInput):
    packages = {
        "вес": "Весовое",
        "фас": "Фасованное"
    }
    strInput = strInput.lower()
    key = next((key for key in packages
                if re.search(rf"\b{re.escape(str(key))}", strInput)), None)
    return packages.get(key, None)

conversionK = {
    "килограмм": 1, "кг": 1, "kg": 1,
    "грамм": 0.001, "гр": 0.001, "г": 0.001, "g": 0.001,
}

# Обозначения веса и чисел в регулярных выражениях
_units = "|".join(sorted(conversionK, key=len, reverse=True))
_num = r"\d+(?:[.,]\d+)?"
_kg = "|".join(sorted(["килограмм", "кг", "kg"], key=len, reverse=True))
_not_in_number = r"(?<!\d)(?<!\d[.,])"

WEIGHT_RE = re.compile(
    rf"{_not_in_number}({_num})\s*({_units})(?![а-яёa-z])"
)
ONLY_KG_RE = re.compile(
    rf"(?<![а-яёa-z\d])({_kg})(?![а-яёa-z])"
)

currentYear = datetime.now().year
def figureWeight(strInput):
    warningMessage = ""
    strInput = strInput.lower()
    found = WEIGHT_RE.search(strInput)
    if found:
        value = float(found.group(1).replace(",", "."))
        if currentYear - 3 < value <= currentYear and found.group(2) == 'г' and value.is_integer():
            warningMessage = "Найденное значение веса похожа на год, рекомендуется проверить вручную."
        elif value * conversionK[found.group(2)] > 50:
            warningMessage = "Найденное значение подозрительно большое, рекомендуется проверить вручную."
        return value * conversionK[found.group(2)], warningMessage

    if ONLY_KG_RE.search(strInput):
        return 1.0, warningMessage

    return None, warningMessage