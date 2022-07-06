# Tim Barnes
# v0.0.6
# 2021-04-06
# Query ifconfig.co for public IP information
from requests import get


def get_data(url):
    return get(url)


def process_data(data):
    return data.json()


def print_connect_error(url):
    print(
        "Unable to reach " + url +
        "\n\nCheck your network connection and retry"
    )


def parse_data(data):
    keys, values = [], []

    for key in data.keys():
        keys.append(key)

    for value in data.values():
        values.append(value)
        
    return keys, values


def print_results(keys, values):
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


def main():
    url = "https://ifconfig.co/json"

    print("\nQuerying " + url + " for your info\n")
    response = get_data(url)

    if("404" in response.text):
        print_connect_error(url)
        exit()

    data = process_data(response)
    keys, values = parse_data(data)[0], parse_data(data)[1]
    print_results(keys, values)


main()
