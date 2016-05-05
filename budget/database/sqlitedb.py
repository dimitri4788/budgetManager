import sqlite3


class Datastore():
    """This class represents data-storage object.

    The Datastore will store all the account information for
    food and miscellaneous accounts.

    Attributes:
        _conn (sqlite3.Connection): A sqlite3.Connection object that represents the database
        _cursor (sqlite3.Cursor): A sqlite3.Cursor object that enables traversal over the records in the database
        _databaseFileName (str): The database filename on the disc
    """

    def __init__(self, dbFileName = None):
        if not dbFileName:
            self._databaseFileName = "example.db"
        else:
            self._databaseFileName = dbFileName

        self._conn = None
        self._cursor = None

    def connect(self):
        """Opens a database connection to the database file and creates tables."""

        try:
            self._conn = sqlite3.connect(self._databaseFileName)
            self._cursor = self._conn.cursor()

            # Create FoodAccount and MiscAccount database tables
            self._cursor.execute("CREATE TABLE IF NOT EXISTS FoodAccount (month text, year text, total real)")
            self._cursor.execute("CREATE TABLE IF NOT EXISTS MiscAccount (month text, year text, total real)")

            # Commit the change
            self._conn.commit()
        except Exception as e:
            self._conn.rollback()
            print "Error: while creating tables FoodAccount and/or MiscAccount:", e

    def disconnect(self):
        """Closes the database connection."""

        # Save (commit) the changes
        self._conn.commit()

        # Close the connection
        self._conn.close()

    def insertFoodAccount(self, month, year, amount):
        """Insert food account details into FoodAccount."""

        try:
            # We can use the sqlite3.Connection object as context manager to automatically commit or rollback transactions
            with self._conn:
                # First get the total amount for the month and year combination
                self._cursor.execute("SELECT total FROM FoodAccount WHERE month=:month and year=:year", {"month": month, "year": year})
                totalList = self._cursor.fetchall()

                # Check if the entry for arguments month and year exists in the database or not
                if not totalList:
                    # Create a new row in FoodAccount for the month and year
                    self._cursor.execute("INSERT INTO FoodAccount VALUES (?, ?, ?)", (month, year, amount))
                else:
                    totalAmount = float(amount) + totalList[0][0]
                    self._cursor.execute("UPDATE FoodAccount SET total = ? WHERE month = ? AND year = ?", (totalAmount, month, year))
        except sqlite3.IntegrityError:
            print "Error: couldn't add to FoodAccount", e

    def insertMiscAccount(self, month, year, amount):
        """Insert misc. account details into MiscAccount."""

        try:
            # We can use the sqlite3.Connection object as context manager to automatically commit or rollback transactions
            with self._conn:
                # First get the total amount for the month and year combination
                self._cursor.execute("SELECT total FROM MiscAccount WHERE month=:month and year=:year", {"month": month, "year": year})
                totalList = self._cursor.fetchall()

                # Check if the entry for arguments month and year exists in the database or not
                if not totalList:
                    # Create a new row in MiscAccount for the month and year
                    self._cursor.execute("INSERT INTO MiscAccount VALUES (?, ?, ?)", (month, year, amount))
                else:
                    totalAmount = float(amount) + totalList[0][0]
                    self._cursor.execute("UPDATE MiscAccount SET total = ? WHERE month = ? AND year = ?", (totalAmount, month, year))
        except sqlite3.IntegrityError:
            print "Error: couldn't add to MiscAccount", e

    def fetchFoodAccount(self):
        """Fetch all the details from FoodAccount."""

        try:
            # We can use the sqlite3.Connection object as context manager to automatically commit or rollback transactions
            with self._conn:
                self._cursor.execute("select * from FoodAccount")
                print self._cursor.fetchall()
        except sqlite3.IntegrityError:
            print "Error: couldn't add to FoodAccount", e

    def fetchMiscAccount(self):
        """Fetch all the details from MiscAccount."""

        try:
            # We can use the sqlite3.Connection object as context manager to automatically commit or rollback transactions
            with self._conn:
                self._cursor.execute("select * from MiscAccount")
                print self._cursor.fetchall()
        except sqlite3.IntegrityError:
            print "Error: couldn't add to MiscAccount", e


db = Datastore()
db.connect()
db.insertFoodAccount("May", "2016", 5.5)
db.insertFoodAccount("May", "2016", 15.3)
db.insertFoodAccount("April", "2016", 10)
db.insertFoodAccount("June", "2016", 5.5)
db.insertFoodAccount("December", "2016", 55)
db.insertFoodAccount("December", "2016", 155)
db.insertFoodAccount("November", "2016", 44.3)
db.insertMiscAccount("October", "2016", 44.3)
db.fetchFoodAccount()
db.fetchMiscAccount()

#TODO Add comments in whole file for each methods and etc.


#XXX
"""
Table
- FoodAccount
    - Columns: month, year, total
- MiscAccount
    - Columns: month, year, total
"""
