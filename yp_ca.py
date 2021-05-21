from requests_html import HTMLSession
import re
import time
import csv
import os
from datetime import date

def get_desktop():
    current_loc = os.getcwd()
    splits = current_loc.split('/')
    return ('/'.join(splits[:3]) + '/Desktop/')


os.chdir(get_desktop())


def writer():
    filename = today + '.csv'
    f = open(filename, 'a', newline='')
    csv_writer = csv.DictWriter(f, fieldnames=head)
    return csv_writer


def csv_headings():
    writer().writeheader()


def cities():
    li = []
    f = open('/Users/han/python/scraping/test_tor/yellowpages/2city_name.txt')
    lines = f.readlines()
    for each in lines:
        li.append((each.strip('\n')))
    return li


def pages():
    lis = []
    base_url = 'https://www.yellowpages.ca/search/si/'
    catagory = ['diamond', 'Jewellers+%26+Jewellery+Stores']
    city = cities()
    for l in catagory:
        for m in city:
            for i in range(1, 10):
                url = base_url + str(i) + '/' + l + '/' + m 
                lis.append(url)
    return lis


def before(url):
    s = HTMLSession()
    r = s.get(url)
    one = r.html.find('div.listing__mlr__root')
    for each in one:
        info = each.find('a')
        try:
            website = re.findall(r"www.+?(?=')", str(info))[0]
            phone = re.findall(r"phone=.+?(?=')", str(info))[0]
            location = re.findall(r"where=.+?(?=&)", str(info))[0]
            data = {"Website" : website, "phone" : phone.strip("'"), 'location' : location}
            writer().writerows([data])
        except:
            pass


head = ['Website', 'phone', 'location']
today = date.today().strftime('%b_%d_%Y')

writer()
csv_headings()

urls = pages()
for l in urls:
    before(l)
    time.sleep(15)
