#This script scrapes, price list of automobiles from the given website.

from bs4 import BeautifulSoup
import requests
import csv
from datetime import datetime
import os
import re


############
# Parsing current date and time to form the output filename.

now = datetime.now()
base_filename = now.strftime("%d%m%Y-%H%M%S")
basefilename = 'TCM-Price_list-'+base_filename
extension ="csv"
dir_name = 'Price-List-Output-Direcotry'
filename = os.path.join(dir_name, basefilename + "." + extension)

data = []

with open("test4.html") as fp:
    soup = BeautifulSoup(fp, 'lxml')

    for dealer, loc in zip(soup.find_all("div", {"class": "main_content"}), soup.find_all("div", {"class": "dearler_loc_btn"})):
        name = dealer.h4.text


        address = dealer.find("span", {"class" : "pl-2 txt_light"}).text
        province = dealer.find("li", {"class": "loc_list2 txt_light"}).text
        province = province.strip()

        # Now Extracting all phone Numbers
        ul_tags = dealer.find_all("ul") # Extracting all UL tags
        n = 3 # As the contact numbers are on 3rd UL
        contact_numbers = ul_tags[n - 1].text  # Subtract 1 as the index starts from 0
        contact_numbers = contact_numbers.replace("UAN", "UAN:")
        contact_numbers = contact_numbers.replace(" ", "")
        contact_numbers = contact_numbers.replace("\n", ":")
        contact_numbers = re.sub(":+", ":", contact_numbers).strip(":")

        # Extracting email addresses
        mailtos = loc.select('a[href^=mailto]')
        for i in mailtos:
            href = i['href']
            email = str(href)
            if "mailto:" in email:
                email = email.replace("mailto:", "")

        # Extracting Website
        website_location = loc.find_all("li")
        web_link = None
        for w in website_location:
            txt = str(w.text)
            if txt.strip() == "Website":
                web_link = w.a['href']

        data.append([name, address, province, contact_numbers, email, web_link])

# Write the data to a CSV file
filename = "output.csv"
with open(filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Address", "Povince", "Contact Numbers", "Email", "Web_link"])  # Write header
    writer.writerows(data)  # Write data rows

print("Data has been written to", filename)