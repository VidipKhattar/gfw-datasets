# access content from website link
import requests

# read, write and format csv file
import csv
import os

# base url containing country data
base_url = "https://data-api.globalforestwatch.org/dataset/gadm__tcl__adm2_summary/latest/query/csv?sql=SELECT iso, adm1, adm2, umd_tree_cover_density__threshold, tsc_tree_cover_loss_drivers__type, umd_tree_cover_extent_2000__ha, umd_tree_cover_extent_2010__ha, area__ha, area__ha, \"umd_tree_cover_gain_2000-2012__ha\" FROM data WHERE iso='"

# create temp csv file
csv_file = open('downloaded.csv', 'ab')

error_iso_codes = []
iso_codes = []

# retrieving iso codes from csv file and reading it into an array
with open('gadm36.csv') as input:
    next(csv.reader(input))
    for row in csv.reader(input):
        if row[0] not in iso_codes:
            iso_codes.append(row[0])


print(f'size of iso is {len(iso_codes)}')
# iterate through the iso code in the array to generate a full url
for iso_indiv in iso_codes:
    complete_url = base_url + iso_indiv + "\'"
    # retrieves data from url
    response = requests.get(complete_url)
    content = response.content
    if content[207:210].decode() in iso_codes:
        csv_file.write(content[204:-1])
        print(f'{iso_indiv} content completed')
    else:
        error_iso_codes.append(iso_indiv)

# removes blank rows from the csv file
with open('downloaded.csv') as input, open('final_summary.csv', 'w', newline='') as output:
    writer = csv.writer(output)
    writer.writerow(['iso', 'adm1', 'adm2', 'umd_tree_cover_density__threshold', 'tsc_tree_cover_loss_drivers__type', 'umd_tree_cover_extent_2000__ha', 'umd_tree_cover_extent_2010__ha', 'umd_tree_cover_gain_2000-2012__ha', 'area__ha'])
    for row in csv.reader(input):
        if any(field.strip() for field in row):
            writer.writerow(row)

# removes unfiltered csv file
print(f'{len(iso_codes)-len(error_iso_codes)} have been added')
print(f'{len(error_iso_codes)} data sets have failed to be retrieved')
print(error_iso_codes)
os.remove('downloaded.csv')
csv_file.close()