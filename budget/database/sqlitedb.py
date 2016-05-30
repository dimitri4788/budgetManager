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

    def __init__(self, dbFileName=None):
        if not dbFileName:
            self._databaseFileName = "budgetManager.db"
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
            gg = self._cursor.execute("CREATE TABLE IF NOT EXISTS FoodAccount (month text, year text, total real)")
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
        """Insert food account details into FoodAccount.

        Args:
            month (str): The month to insert the amount to
            year (str): The year to insert the amount to
            amount (float): The amount to be inserted
        """

        try:
            # NOTE: We can use the sqlite3.Connection object as context manager to automatically commit or rollback transactions
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
        """Insert misc. account details into MiscAccount.

        Args:
            month (str): The month to insert the amount to
            year (str): The year to insert the amount to
            amount (float): The amount to be inserted
        """

        try:
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

    def fetchFoodAccount(self, month=None, year=None):  # NOTE: This method can combined with insertMiscAccount to refactor the code
        """Fetch the details from FoodAccount.

         Args:
            month (str): The month to fetch amount from
            year (str): The year to fetch amount from
        """
        if month is None or year is None:
            return str(-1)  # Error case
        else:
            try:
                with self._conn:
                    self._cursor.execute("SELECT total FROM FoodAccount WHERE month=:month and year=:year", {"month": month, "year": year})
                    totalAmount = self._cursor.fetchall()
                    if not totalAmount:
                        return 0.0
                    else:
                        return totalAmount[0][0]
            except sqlite3.IntegrityError:
                print "Error: couldn't fetch from the FoodAccount", e
                return str(-1)  # Error case

    def fetchMiscAccount(self, month=None, year=None):
        """Fetch the details from MiscAccount.

         Args:
            month (str): The month to fetch amount from
            year (str): The year to fetch amount from
        """

        if month is None or year is None:
            return str(-1)  # Error case
        else:
            try:
                with self._conn:
                    self._cursor.execute("SELECT total FROM MiscAccount WHERE month=:month and year=:year", {"month": month, "year": year})
                    totalAmount = self._cursor.fetchall()
                    if not totalAmount:
                        return 0.0
                    else:
                        return totalAmount[0][0]
            except sqlite3.IntegrityError:
                print "Error: couldn't fetch from the MiscAccount", e
                return str(-1)  # Error case

    def fetchAllFoodAccount(self):
        """Fetch everything from FoodAccount."""

        try:
            with self._conn:
                self._cursor.execute("SELECT * FROM FoodAccount")
                allAccount = self._cursor.fetchall()
                if not allAccount:
                    return []
                return allAccount
        except sqlite3.IntegrityError:
            print "Error: couldn't fetch from the FoodAccount", e
            return []  # Error case

    def fetchAllMiscAccount(self):
        """Fetch everything from MiscAccount."""

        try:
            with self._conn:
                self._cursor.execute("SELECT * FROM MiscAccount")
                allAccount = self._cursor.fetchall()
                if not allAccount:
                    return []
                return allAccount
        except sqlite3.IntegrityError:
            print "Error: couldn't fetch from the MiscAccount", e
            return []  # Error case

# XXX
#db = Datastore()
#db.connect()
#db.insertFoodAccount("January", "2016", 35.5)
#db.insertFoodAccount("February", "2016", 5)
#db.insertFoodAccount("March", "2016", 45)
#db.insertFoodAccount("April", "2016", 95)
#db.insertFoodAccount("May", "2016", 5.5)
##db.insertMiscAccount("May", "2016", 44.3)
##db.insertMiscAccount("May", "2016", 44.3)
##print db.fetchFoodAccount("May", "2016")
#print db.fetchAllFoodAccount()
