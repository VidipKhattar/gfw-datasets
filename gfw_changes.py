# access content from website link
import requests

# read, write and format csv file
import csv
import os

# create temp csv file
csv_file = open('downloaded.csv', 'ab')

# fixed parts of the url link containing csv file
base_url = "https://data-api.globalforestwatch.org/dataset/gadm__tcl__adm2_change/latest/query/csv?sql=SELECT iso, adm1::integer, adm2::integer, umd_tree_cover_loss__year, SUM(umd_tree_cover_loss__ha) FROM data WHERE iso='"

post_iso_url = "' AND umd_tree_cover_density__threshold=30 GROUP BY umd_tree_cover_loss__year, iso, adm1, adm2 ORDER BY iso, adm1, adm2"

error_iso_codes = []
iso_codes = []

#retrieving iso codes from csv file and reading it into an array
with open('gadm36.csv') as input:
    next(csv.reader(input))
    for row in csv.reader(input):
        if row[0] not in iso_codes:
            iso_codes.append(row[0])


print(f'size of iso is {len(iso_codes)}')
# iterate through the iso code in the array to generate a full url
for iso_indiv in iso_codes:
    complete_url = base_url + iso_indiv + post_iso_url
    # retrieves data from url through a request
    response = requests.get(complete_url)
    content = response.content
    if content[56:59].decode() in iso_codes:
        csv_file.write(content[53:-1])
        print(f'{iso_indiv} content completed')
    else:
        error_iso_codes.append(iso_indiv)

# removes blank rows from the csv file
with open('downloaded.csv') as input, open('final_changes.csv', 'w', newline='') as output:
    writer = csv.writer(output)
    writer.writerow(['iso', 'adm1', 'adm2', 'umd_tree_cover_loss__year', 'sum'])
    for row in csv.reader(input):
        if any(field.strip() for field in row):
            writer.writerow(row)

# removes unfiltered csv file
print(f'{len(iso_codes)-len(error_iso_codes)} have been added')
print(f'{len(error_iso_codes)} data sets have failed to be retrieved')
print(error_iso_codes)
os.remove('downloaded.csv')
csv_file.close()
