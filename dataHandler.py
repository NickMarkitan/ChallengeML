import re

def decomposeDecription(strInput, varAliasesDict):
    """Возвращает набор параметров взятых из введённой строки"""
    strInput = strInput.lower()
    return findAliases(strInput, varAliasesDict), confirmIsApple(strInput), checkColor(strInput), checkPackageType(strInput), figureWeight(strInput)

def findAliases(strInput, varAliasesDict):
    """Ищет в строке участки совпадающие с ключами передоваемого словаря и возвращает соответствующее значение словаря (первое совпадение)
    Предполагается для использования со словарём Алиас -> Полное название сорта"""
    key = next((key for key in varAliasesDict
        if re.search(rf"\b{re.escape(str(key))}\b", strInput)), None)
    return varAliasesDict[key] if key is not None else "NaN"

def confirmIsApple(strInput):
    """Ищет в строке участки похожие на упоминание яблок и возвращает 'Яблоки' если находит что-то подходящее"""
    return "Яблоки" if re.search(r"\bяблок", strInput, flags=re.IGNORECASE) else "Nan"

def checkColor(strInput):
    """Ищет в строке участки похожие на упоминание цвета яблок и возвращает универсальное полное слово первого найденого цвета"""
    colors = {
        "зелен": "Зеленый",
        "красн": "Красный",
        "желт": "Желтый",
    }
    strInput = strInput.lower().replace("ё", "е")
    key = next((key for key in colors
                if re.search(rf"\b{re.escape(str(key))}", strInput)), None)
    return colors.get(key, "NaN")

def checkPackageType(strInput):
    packages = {
        "вес": "Весовое",
        "фас": "Фасованное"
    }
    strInput = strInput.lower()
    key = next((key for key in packages
                if re.search(rf"\b{re.escape(str(key))}", strInput)), None)
    return packages.get(key, "NaN")


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

def figureWeight(strInput):
    strInput = strInput.lower()
    found = WEIGHT_RE.search(strInput)
    if found:
        value = float(found.group(1).replace(",", ".")) if found.group(1) else 1.0
        return value * conversionK[found.group(2)]

    if ONLY_KG_RE.search(strInput):
        return 1.0

    return "NaN"