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
$ git clone 
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
block under the <p> tag. So the following python code that I used:

```
def write_csv():
    """Write the list of Wake Med addresses into a CSV file"""
    address_list = get_address()
    with open('address.csv', 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(address_list)
write_csv()

```

generated a csv file (address.csv) where all the lines ran into each other -- the address, telephone etc. Also, the WakeMed site does not have uniformity in the way the addresses are listed on their site (this can be fixed with python code) so 
I finally fixed the csv file by hand before going ahead with the program. I also had to manually remove the map and directions section, which again runs into the other lines, all inside the <p> tag. 

If you run all the lines of my code, you will have to fix the address.csv by hand like I did. I still haven't worked out the correct way of doing this to generate the file as I want it. So ideally, do not run the above function, but instead use the file that I have manually fixed, which is there in the repository.

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

Again the latlong.csv file that I generate with this code:

```
def write_csv2():
    """Write the list of Wake Med addresses into a CSV file"""
    latlong = get_latlong()
    with open('latlong.csv', 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(latlong)

write_csv2()
```

is not breaking into separate lines, so there is some flaw in my code that I still need to fix. Since my focus was
to generate the file with the geographical coordinates attached to the addresses, I fixed this csv file by hand also. Again I suggest you just use the fixed latlong.csv file in my repository and move forward with this code using the pandas library:


```
def get_address_latlong():
    a = pd.read_csv("address.csv")
    b = pd.read_csv("latlong.csv")
    b = b.dropna(axis=1)
    merged = a.merge(b, on='zip')
    merged.to_csv("output.csv", index=False)
get_address_latlong()

```

The above code generates the output.csv file that has all the addresses and geographical coordinates for the emergency care centers in Wake County. I am building an app with jQuery and Leaflet.js to use this file, which will show the nearest emergency care center in Wake County to the address typed in by users on the frontend. As soon as the app is ready, I will paste the link to it here.






