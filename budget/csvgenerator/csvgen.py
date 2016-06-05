import csv
import sys


def genCSV(dbHandle=None, fileLocation=None):
    """Generates CSV (comma separated) file with the full account details."""

    if not dbHandle:
        sys.exit("Error: dbHandle passed to genCSV() is None")

    fileName = "accounts.csv"
    if fileLocation:
        fileName = fileLocation + "/" + "accounts.csv"

    with open(fileName, 'w') as csvfile:
        fieldNameForFoodAccount = ['Food Account']
        writerFoodField = csv.DictWriter(csvfile, fieldnames=fieldNameForFoodAccount)

        fieldNameForMiscAccount = ['Misc. Account']
        writerMiscField = csv.DictWriter(csvfile, fieldnames=fieldNameForMiscAccount)

        fieldNamesCommon = ['Month', 'Year', 'Total ($)']
        writerCommon = csv.DictWriter(csvfile, fieldnames=fieldNamesCommon)

        # Write food header
        writerFoodField.writeheader()

        # Write common header-fields to the file
        writerCommon.writeheader()

        # Get whole food and misc account
        foodAccount = dbHandle.fetchAllFoodAccount()
        miscAccount = dbHandle.fetchAllMiscAccount()

        # Write food account rows to the file
        for foodRow in foodAccount:
            writerCommon.writerow({'Month': foodRow[0], 'Year': foodRow[1], 'Total ($)': foodRow[2]})

        # Write two blank lines
        writerCommon.writerow({'Month': "", 'Year': "", 'Total ($)': ""})
        writerCommon.writerow({'Month': "", 'Year': "", 'Total ($)': ""})

        # Write misc. header
        writerMiscField.writeheader()

        # Write common header-fields to the file
        writerCommon.writeheader()

        # Write misc. account rows to the file
        for miscRow in miscAccount:
            writerCommon.writerow({'Month': miscRow[0], 'Year': miscRow[1], 'Total ($)': miscRow[2]})
