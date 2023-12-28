import requests
from bs4 import BeautifulSoup
import pandas as pd

# Upgrade certifi
try:
    import certifi
    certifi.old_where = certifi.where
    certifi.where = lambda: certifi.old_where() + "\\cacert.pem"
    requests.get('https://www.google.com', verify=True)  # This line triggers the certificate upgrade
except Exception as e:
    print(f"Error upgrading certifi: {e}")

# Replace 'URL' with the URL of the webpage containing the tables
url = 'https://kshec.karnataka.gov.in/info-4/State+Universities+List/en'

# Send an HTTP request to the URL with SSL verification disabled
try:
    response = requests.get(url, verify=True)
except requests.exceptions.SSLError:
    response = requests.get(url, verify=False)

# Parse the HTML content of the page using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all tables on the webpage
tables = soup.find_all('table')

# Initialize an empty list to store table data
all_tables_data = []

# Loop through each table
for table in tables:
    # Extract data from each row of the table
    table_data = []
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all(['td', 'th'])
        cols = [col.text.strip() for col in cols]
        table_data.append(cols)

    # Append the table data to the list
    all_tables_data.append(table_data)

# Create an Excel writer using pandas
excel_writer = pd.ExcelWriter('output.xlsx', engine='openpyxl')

# Loop through each table data and write it to a separate sheet
for i, table_data in enumerate(all_tables_data):
    df = pd.DataFrame(table_data)
    sheet_name = f'Table_{i+1}'
    df.to_excel(excel_writer, sheet_name=sheet_name, index=False, header=False)

# Save the Excel file
excel_writer._save()
print('Data has been scraped and saved to output.xlsx')



