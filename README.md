# ScrapeWithPython

## Overview:

A Python program to scrape a web page and result in a csv file. 

## Resources:

1. Requests library to make http requests to the webpage
2. BeautifulSoup4 library to webscrape
3. Pandas
3. CSV

## Installation:
Project requires Python 3.6.8 and pip 19.1.1

```
$ git clone https://github.com/SowmyaAji/ScrapeWithPython.git
$ pipenv shell
$ pip install -r requirements.txt

```
## How it works:

run from the command line:

```
$ python scraper.py

```

## Output:

A file output.csv is generated with a list of Emergency Help Centers in Wake County, their addresses,
phone numbers and geographical coordinates. 

## Issues:

The program uses Beautiful Soup 4 to scrape from the WakeMed website:

"https://www.wakemed.org/emergency-trauma-locations

However, I still haven't worked out the code to separate the individual parts of the address from
the overall <p> tag, as each element does not have css classes or tags on them, making all of them one 
block under the <p> tag. 

I ended u generating a csv file (address1.csv) where all the lines ran into each other -- the address, telephone etc. Also, the WakeMed site does not have uniformity in the way the addresses are listed on their site (this can be fixed with python code) so 
I finally fixed the csv file (address.csv) by hand before going ahead with the program. I also had to manually remove the map and directions section, which again runs into the other lines, all inside the <p> tag. I am still working on fixing this problem.


The next csv file that I generate, latlong.csv, uses a list of latitudes and logitudes in the US, taken from Erichrust's gist here:

https://gist.github.com/erichurst/7882666#file-us-zip-codes-from-2013-government-data

I use this series of python functions to generate that file (it is much easier with pandas, but I wanted to try this out):

```
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
    return [item['zip'] for item in get_address_list()]


def get_latlong():
    address = get_zips()
    address_latlong = []
    latlong = get_rows("uslatlongfull.csv")
    for row in latlong:
        if (row['zip']).strip() in address:
            address_latlong.append(
                row['zip'].strip() + "," + row['lat'] + "," + row['lng'] + "\n")
    return address_latlong
```

For the final csv file, I just used the pandas library, which is really the easiest way:


```
def get_address_latlong():
    a = pd.read_csv("address.csv")
    b = pd.read_csv("latlong.csv")
    b = b.dropna(axis=1)
    merged = a.merge(b, on='zip')
    merged.to_csv("output.csv", index=False)
get_address_latlong()

```

The above code generates the output.csv file that has all the addresses and geographical coordinates for the emergency care centers in Wake County. I am have built an app with jQuery and Leaflet.js to use this file, which will show the nearest emergency care center in Wake County to the address typed in by users on the frontend. Here is the link to the webpage hosting the app: https://sowmyaaji.github.io/find_help.html

And here is the link to the repository of that app: https://github.com/SowmyaAji/MedHelpNearMe





