import csv

def genCSV(dbHandle=None):
    """
    with open('accounts.csv', 'w') as csvfile:
        fieldnames = ['first_name', 'last_name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
        writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
        writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})
    """
    with open('accounts.csv', 'w') as csvfile:
        fNames = ['Month', 'Year', 'Total ($)']
        writer = csv.DictWriter(csvfile, fieldnames=fNames)

        writer.writeheader()
        xx = dbHandle.fetchFoodAccount(month="May", year="2016")
        writer.writerow({'Month': 'May', 'Year': '2016', 'Total ($)': xx})
