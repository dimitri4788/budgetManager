#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import sys

from PyQt4 import QtCore
from PyQt4 import QtGui

from csvgenerator import *
from database import *


class BudgetWidget(QtGui.QWidget):
    """This is the main Budget widget class which encapsulates the whole app."""

    # First get the handle to Datastore (all the instances of BudgetWidget share dbHandle; it is a class member)
    dbHandle = Datastore()
    dbHandle.connect()

    def __init__(self):
        # First construct QWidget
        super(self.__class__, self).__init__()

        # Dictionary mapping months to indices
        hashMapOfMonths = {'January': 0, 'February': 1, 'March': 2, 'April': 3, 'May': 4, 'June': 5, 'July': 6, 'August': 7, 'September': 8, 'October': 9, 'November': 10, 'December': 11}

        # Create labels
        self.header = QtGui.QLabel("Budget Manager", self)
        now = datetime.datetime.now()
        hashMapCurrentMonthIndex = hashMapOfMonths[now.strftime('%B')]
        self.currentTotal = QtGui.QLabel("Current Total", self)
        self.foodLabel = QtGui.QLabel("Food", self)
        self.miscLabel = QtGui.QLabel("Miscellaneous", self)
        self.foodLabelTotalValue = QtGui.QLabel("000000000000000000", self)  # Hack to make label long
        self.miscLabelTotalValue = QtGui.QLabel("000000000000000000", self)  # Hack to make label long

        # Set drop-down list for months
        self.comboBoxMonth = QtGui.QComboBox(self)
        self.comboBoxMonth.addItem("January")
        self.comboBoxMonth.addItem("February")
        self.comboBoxMonth.addItem("March")
        self.comboBoxMonth.addItem("April")
        self.comboBoxMonth.addItem("May")
        self.comboBoxMonth.addItem("June")
        self.comboBoxMonth.addItem("July")
        self.comboBoxMonth.addItem("August")
        self.comboBoxMonth.addItem("September")
        self.comboBoxMonth.addItem("October")
        self.comboBoxMonth.addItem("November")
        self.comboBoxMonth.addItem("December")
        self.comboBoxMonth.setCurrentIndex(hashMapCurrentMonthIndex)  # Set current display month

        # Set drop-down list for years
        listOfThreeYear = []  # Will hold previous, current, next year
        listOfThreeYear.append(str(int(now.strftime('%Y'))-1))
        listOfThreeYear.append(str(int(now.strftime('%Y'))))
        listOfThreeYear.append(str(int(now.strftime('%Y'))+1))
        self.comboBoxYear = QtGui.QComboBox(self)
        for year in listOfThreeYear:
            self.comboBoxYear.addItem(year)
        self.comboBoxYear.setCurrentIndex(listOfThreeYear.index(now.strftime('%Y')))  # Set current display year

        # Set action method to be called when month/year comboBox is changed
        self.comboBoxMonth.activated[str].connect(self.updateTotalValuesMethod)
        self.comboBoxYear.activated[str].connect(self.updateTotalValuesMethod)

        # Create line-edits
        self.foodLineedit = QtGui.QLineEdit(self)
        self.miscLineedit = QtGui.QLineEdit(self)

        # Create push-buttons
        self.submitButton = QtGui.QPushButton('Submit', self)
        self.csvButton = QtGui.QPushButton('Generate CSV', self)

        # Set labels positions
        self.header.move(130, 20)
        self.header.setStyleSheet('font-size: 18px')
        self.comboBoxMonth.move(95, 43)
        self.comboBoxYear.move(213, 43)
        self.currentTotal.move(280, 75)
        self.foodLabel.move(5, 95)
        self.foodLabel.setStyleSheet('font-weight: bold')
        self.miscLabel.move(5, 115)
        self.miscLabel.setStyleSheet('font-weight: bold')
        self.foodLabelTotalValue.move(300, 95)
        self.miscLabelTotalValue.move(300, 115)

        # Set line-edits positions and size
        self.foodLineedit.move(100, 90)
        self.foodLineedit.resize(90, 20)
        self.miscLineedit.move(100, 110)
        self.miscLineedit.resize(90, 20)

        # Set position of submitButton and the action associated with it
        self.submitButton.move(117, 160)
        self.submitButton.clicked.connect(self.submitButtonClicked)
        self.submitButton.setStyleSheet("background-color: #FFB90F; border-style: outset; border-width: 2px; border-radius: 10px; border-color: beige; font: bold 14px; min-width: 10em; padding: 6px")

        # Set position of csvButton and the action associated with it
        self.csvButton.move(117, 190)
        self.csvButton.clicked.connect(self.csvButtonClicked)
        self.csvButton.setStyleSheet("background-color: green; border-style: outset; border-width: 2px; border-radius: 10px; border-color: beige; font: bold 14px; min-width: 10em; padding: 6px")

        # Set app window size, title, background color and center the widget on the screen
        widgetWidth = 380
        widgetHeight = 230
        desktopSize = QtGui.QApplication.desktop().availableGeometry(self)
        desktopWidth = desktopSize.getRect()[2]
        desktopHeight = desktopSize.getRect()[3]
        widgetX = (desktopWidth - widgetWidth) / 2
        widgetY = (desktopHeight - widgetHeight) / 2
        self.setGeometry(widgetX, widgetY, widgetWidth, widgetHeight)
        self.setWindowTitle('Budget Manager')
        colorPalette = self.palette()
        colorPalette.setColor(QtGui.QPalette.Background, QtGui.QColor(67, 205, 128))
        self.setPalette(colorPalette)
        self.show()

        # Fill the food label total value with the current total amount for food and misc
        currentMonth = now.strftime('%B')
        currentYear = now.strftime('%Y')
        currFoodTotal = BudgetWidget.dbHandle.fetchFoodAccount(currentMonth, currentYear)
        currMiscTotal = BudgetWidget.dbHandle.fetchMiscAccount(currentMonth, currentYear)
        self.foodLabelTotalValue.setText(str(currFoodTotal))
        self.miscLabelTotalValue.setText(str(currMiscTotal))

    def updateTotalValuesMethod(self, text):
        """This method gets called when user changes combobox values for month/year.

        It updates the total value of food/misc display on the widget.
        """

        # Get the current selected month and year
        currentSelectedMonth = str(self.comboBoxMonth.currentText())
        currentSelectedYear = str(self.comboBoxYear.currentText())

        # Set the value labels
        currFoodTotal = BudgetWidget.dbHandle.fetchFoodAccount(currentSelectedMonth, currentSelectedYear)
        currMiscTotal = BudgetWidget.dbHandle.fetchMiscAccount(currentSelectedMonth, currentSelectedYear)
        self.foodLabelTotalValue.setText(str(currFoodTotal))
        self.miscLabelTotalValue.setText(str(currMiscTotal))

    def submitButtonClicked(self):
        """This method gets called when the user presses the submit button.

        It updates the database based on the user entered values and also
        updates the display on the widget.
        """

        # Get the user entered values
        foodValueEnteredByUser = self.foodLineedit.text()
        miscValueEnteredByUser = self.miscLineedit.text()
        if not foodValueEnteredByUser:
            foodValueEnteredByUser = 0.0
        else:
            foodValueEnteredByUser = float(foodValueEnteredByUser)
        if not miscValueEnteredByUser:
            miscValueEnteredByUser = 0.0
        else:
            miscValueEnteredByUser = float(miscValueEnteredByUser)

        # Get the current selected month and year
        currentSelectedMonth = str(self.comboBoxMonth.currentText())
        currentSelectedYear = str(self.comboBoxYear.currentText())

        # Set the value labels
        currFoodTotal = BudgetWidget.dbHandle.fetchFoodAccount(currentSelectedMonth, currentSelectedYear) + foodValueEnteredByUser
        currMiscTotal = BudgetWidget.dbHandle.fetchMiscAccount(currentSelectedMonth, currentSelectedYear) + miscValueEnteredByUser
        self.foodLabelTotalValue.setText(str(currFoodTotal))
        self.miscLabelTotalValue.setText(str(currMiscTotal))

        # Update the database with the entered values
        BudgetWidget.dbHandle.insertFoodAccount(currentSelectedMonth, currentSelectedYear, foodValueEnteredByUser)
        BudgetWidget.dbHandle.insertMiscAccount(currentSelectedMonth, currentSelectedYear, miscValueEnteredByUser)

        # Clear the line-edits
        self.foodLineedit.clear()
        self.miscLineedit.clear()

    def csvButtonClicked(self):
        """This method gets called when the user presses the CSV generator button.

        It calls the genCSV() method to generator the CSV file.
        """

        # First get the location where file needs to be saved
        fLocation = QtGui.QFileDialog.getExistingDirectory(self, 'File Location', '/home', QtGui.QFileDialog.ShowDirsOnly)

        # Now call the generate csv function to generate the csv file
        genCSV(BudgetWidget.dbHandle, fLocation)


def main():
    """This function is where the budget app starts."""

    app = QtGui.QApplication(sys.argv)
    ex = BudgetWidget()
    sys.exit(app.exec_())


# Execute only if run as a script
if __name__ == "__main__":
    main()
