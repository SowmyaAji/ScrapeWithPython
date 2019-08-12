import requests
import pdb
from bs4 import BeautifulSoup
import csv
import pandas as pd


def get_address():
    """Using Beautiful Soup, scrape the Wake Med webpage to get a list of Emergency centers"""
    url = "https://www.wakemed.org/emergency-trauma-locations"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    addresses = soup.find_all('p')
    address_list = []
    for i in range(17, len(addresses)):
        addresses = soup.find_all('p')[i].text
        address_list.append(addresses)
    return address_list


def write_csv():
    """Write the list of Wake Med addresses into a CSV file"""
    address_list = get_address()
    with open('address.csv', 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(address_list)


# write_csv()
def get_rows(file):
    """Open csv files and return the data"""
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)


def get_address_list():
    address = get_rows('address.csv')
    return address


def get_zips():
    """Get the zipcodes"""
    return [(item['Zip']).strip() for item in get_address_list()]


print(get_zips())


def get_latlong():
    address = get_zips()
    address_latlong = []
    latlong = get_rows("uslatlongfull.csv")
    for row in latlong:
        if row['Zip'] in address:
            address_latlong.append(
                row['Zip'].strip() + "," + row['Lat'] + "," + row['Lng'])
    return address_latlong


def print_csv2():
    output = get_latlong()
    with open('latlong.csv', 'w') as f:
        f.write('Zip,Latitude,Longitude\n')
        f.write("\n".join(output))


# print_csv2()


def get_address_latlong():
    a = pd.read_csv("address.csv")
    b = pd.read_csv("latlong.csv")
    b = b.dropna(axis=1)
    merged = a.merge(b, on='Zip')
    merged.to_csv("output.csv", index=False)


get_address_latlong()
