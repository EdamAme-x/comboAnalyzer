import re as regex
from urllib.parse import urlparse
from collections import Counter

comboBase: str = open("./sample.txt", "r").read()
comboLines: list = comboBase.split("\n")

database: dict = {
    "list": [],
    "mails": []
}

def isMail(name: str) -> bool:
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return regex.match(pattern, name) is not None

def isURL(url: str) -> bool:
    try:
        result = urlparse(url)
        return True
    except ValueError:
        return False

def parseToHost(url: str):
    if isURL(url):
        parsedURL = urlparse(url)
        host = parsedURL.netloc
        return host
    else:
        return False

def hyperSplit(line: str) -> list:
    line = line.replace("://", "_X_@P_X_//")
    result = line.split(":")
    result[0] = result[0].replace("_X_@P_X_//", "://")
    return result

for line in comboLines:
    lineInfo: list = hyperSplit(line)
    if len(lineInfo) != 3:
        continue
    host = parseToHost(lineInfo[0])
    mail = isMail(lineInfo[1])
    if host is not False:
        database["list"].append(host)
    
    if mail:
        database["mails"].append(lineInfo[1])

def removeSameValue(array: list) -> list:
    return list(set(array))

def rankingStrings(data_list: list) -> list:
    counts = Counter(data_list)
    
    sortedCounts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    
    ranking = [{"value": value, "count": count} for value, count in sortedCounts]
    
    return ranking

result: dict = {
    "mails": removeSameValue(database["mails"]),
    "hosts": rankingStrings(database["list"])
}

def createResult(result: dict) -> dict:
    hostResult: str = ""
    
    hostResult += f"=== ComboResult ===\n"
    hostResult += f"\n"
    hostResult += f"Github: EdamAme-x/ComboAnalyzer\n"
    hostResult += f"総ホスト数: {len(result['hosts'])}\n"
    hostResult += f"\n"
    hostResult += f"=== ComboResult ===\n"

    count = 0

    for host in result["hosts"]:
        count += 1
        hostResult += f"{str(count)}. {host['value']} : {host['count']}\n"

    mailResult: str = ""

    mailResult += f"=== Mail Result ===\n"
    mailResult += f"\n"
    mailResult += f"Github: EdamAme-x/ComboAnalyzer\n"
    mailResult += f"総メール数: {len(result['mails'])}\n"
    mailResult += f"\n"
    mailResult += f"=== Mail Result ===\n"
    for mail in result["mails"]:
        mailResult += f"{mail}\n"

    return {
        "host": hostResult,
        "mail": mailResult
    }


Result: dict = createResult(result)

with open("host_result.txt", "w+") as hostFile:
    hostFile.write(Result["host"])

with open("mail_result.txt", "w+") as mailFile:
    mailFile.write(Result["mail"])