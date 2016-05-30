import csv

def genCSV(dbHandle=None):
    """Generates CSV (comma separated) file with the full acount details."""

    with open('accounts.csv', 'w') as csvfile:
        fNames = ['Month', 'Year', 'Total ($)']
        writer = csv.DictWriter(csvfile, fieldnames=fNames)

        # Write headers field to the file
        writer.writeheader()

        # Get whole food and misc account
        foodAccount = dbHandle.fetchAllFoodAccount()
        miscAccount = dbHandle.fetchAllMiscAccount()

        for foodRow in foodAccount:
            print "foodRow[0]: ", foodRow[0]
            print "foodRow[1]: ", foodRow[1]
            print "foodRow[2]: ", foodRow[2]
            writer.writerow({'Month': foodRow[0], 'Year': foodRow[1], 'Total ($)': foodRow[2]})

        writer.writerow({'Month': "", 'Year': "", 'Total ($)': ""})
        writer.writerow({'Month': "", 'Year': "", 'Total ($)': ""})

        for miscRow in miscAccount:
            writer.writerow({'Month': miscRow[0], 'Year': miscRow[1], 'Total ($)': miscRow[2]})


    #ff = dbHandle.fetchAllMiscAccount()
    #ff = dbHandle.fetchAllFoodAccount()
    #print "ff: ", ff
    #print "ff[0]: ", ff[0]
    #print "ff[0]: ", ff[0][0]
    #print "ff[1]: ", ff[1]
    #print "ff[1]: ", ff[1][1]
    #print "type(ff[1]): ", type(ff[1][1])
