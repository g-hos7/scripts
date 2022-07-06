# Author: Tim Barnes
# Version: 0.0.6
# 2021-04-06
# Query ifconfig.co for public IP information
from requests import get

def main():
    url = "https://ifconfig.co/json"

    print("\nQuerying " + url + " for your info\n")
    response = getData(url)

    if("404" in response.text):
        printConnectErr(url)
        exit()

    data = processData(response)
    keys, values = parseData(data)[0], parseData(data)[1]
    printResults(keys, values)

def getData(url):
    return get(url)

def processData(data):
    return data.json()

def printConnectErr(url):
    print(
        "Unable to reach " + url +
        "\n\nCheck your network connection and retry"
    )

def parseData(data):
    keys, values = [], []

    for key in data.keys():
        keys.append(key)

    for value in data.values():
        values.append(value)
        
    return keys, values

def printResults(keys, values):
    fields = {
        "ip": "IP Address", "country": "Country", "region_name": "Region",
        "zip_code": "Zip Code", "city": "City", "time_zone": "Time Zone"
    }

    for i in range(len(keys)):
        if(keys[i] in fields):
            print(
                str(fields.get(keys[i])).ljust(15) +
                str(values[i]).ljust(0)
            )
        else:
            continue

main()
