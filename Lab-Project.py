import requests
from bs4 import BeautifulSoup
import pandas as pd
from IPython.display import display

# Retrieve the webpage
url = "https://www.indiacustomercare.com/s-v-nit-surat-contact-no"

response = requests.get(url)
soup = BeautifulSoup(response.content, "lxml")
tables = soup.find_all("table")

for table in tables:
    # Creating a list of Dictionaries

    table_data = []

    rows = table.find_all("tr")
    for row in rows:
        columns = row.find_all("td")
        # print(columns)
        column_data = {}
        for i, column in enumerate(columns):
            # use headers as key
            header = table.find_all("th")[i].text if table.find_all("th") else i
            column_data[header] = column.text.replace("\n", "").replace("   ", "")
            # print(column.text)
        table_data.append(column_data)


    # convert list of dictionaries into pandas DataFrame

    df = pd.DataFrame(table_data)

    # Since the first row in an html table consists purely of headers, first column_data is an empty
    # dictionary, which when appended in the list table_data, gives such a result:

    # [{}, {'Name' : 'Dr. Hitesh. R. Jariwala', 'Designation' : 'Centre In-charge', 'Number'...]

    # This empty dictionary is problematic because when fed into a DataFrame (like df), pandas
    # recognises this as a valid row of the table and fills the data with NaN wherever
    # applicable. So we drop the first row. :)
    df.drop(0, inplace=True)

    display(df)
    print('')
    print('')
