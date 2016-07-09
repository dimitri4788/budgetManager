#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import sys

from PyQt4 import QtGui

from csvgenerator import *
from database import *


# Global data
hashMapOfMonths = { 'January' : 0, 'February' : 1, 'March' : 2, 'April' : 3, 'May' : 4, 'June' : 5, 'July' : 6, 'August' : 7, 'September' : 8, 'October' : 9, 'November' : 10, 'December' : 11}

class BudgetWidget(QtGui.QWidget):
    """This is the main Budget widget class which encapsulates the whole app."""

    # First get the handle to Datastore (all the instances of BudgetWidget share dbHandle; it is a class member)
    dbHandle = Datastore()
    dbHandle.connect()

    def __init__(self):
        # First construct QWidget
        super(self.__class__, self).__init__()

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
        self.comboBox = QtGui.QComboBox(self)
        self.comboBox.addItem("January")
        self.comboBox.addItem("February")
        self.comboBox.addItem("March")
        self.comboBox.addItem("April")
        self.comboBox.addItem("May")
        self.comboBox.addItem("June")
        self.comboBox.addItem("July")
        self.comboBox.addItem("August")
        self.comboBox.addItem("September")
        self.comboBox.addItem("October")
        self.comboBox.addItem("November")
        self.comboBox.addItem("December")
        self.comboBox.activated[str].connect(self.styleChoiceMethod)
        self.comboBox.setCurrentIndex(hashMapCurrentMonthIndex)  # Set current display month

        # XXX
        self.styleChoice = QtGui.QLabel("Windows Vista", self)
        self.styleChoice.move(50,150)
        # XXX



        # Create line-edits
        self.foodLineedit = QtGui.QLineEdit(self)
        self.miscLineedit = QtGui.QLineEdit(self)

        # Create push-buttons
        self.submitButton = QtGui.QPushButton('Submit', self)
        self.csvButton = QtGui.QPushButton('Generate CSV', self)

        # Set labels positions
        self.header.move(130, 20)
        self.header.setStyleSheet('font-size: 18px')
        self.comboBox.move(160, 43)
        self.currentTotal.move(280, 60)
        self.foodLabel.move(5, 80)
        self.foodLabel.setStyleSheet('font-weight: bold')
        self.miscLabel.move(5, 100)
        self.miscLabel.setStyleSheet('font-weight: bold')
        self.foodLabelTotalValue.move(300, 80)
        self.miscLabelTotalValue.move(300, 100)

        # Set line-edits positions and size
        self.foodLineedit.move(100, 80)
        self.foodLineedit.resize(90, 20)
        self.miscLineedit.move(100, 100)
        self.miscLineedit.resize(90, 20)

        # Set position of submitButton and the action associated with it
        self.submitButton.move(117, 150)
        self.submitButton.clicked.connect(self.submitButtonClicked)
        self.submitButton.setStyleSheet("background-color: red; border-style: outset; border-width: 2px; border-radius: 10px; border-color: beige; font: bold 14px; min-width: 10em; padding: 6px")

        # Set position of csvButton and the action associated with it
        self.csvButton.move(117, 180)
        self.csvButton.clicked.connect(self.csvButtonClicked)
        self.csvButton.setStyleSheet("background-color: green; border-style: outset; border-width: 2px; border-radius: 10px; border-color: beige; font: bold 14px; min-width: 10em; padding: 6px")

        # Set app window size and title and center the widget on the screen
        widgetWidth = 380
        widgetHeight = 230
        desktopSize = QtGui.QApplication.desktop().availableGeometry(self)
        desktopWidth = desktopSize.getRect()[2]
        desktopHeight = desktopSize.getRect()[3]
        widgetX = (desktopWidth - widgetWidth) / 2
        widgetY = (desktopHeight - widgetHeight) / 2
        self.setGeometry(widgetX, widgetY, widgetWidth, widgetHeight)
        self.setWindowTitle('Budget Manager')
        self.show()

        # Fill the line-edits with the amount for food and misc
        currentMonth = now.strftime('%B')
        currentYear = now.strftime('%Y')
        currFoodTotal = BudgetWidget.dbHandle.fetchFoodAccount(currentMonth, currentYear)
        currMiscTotal = BudgetWidget.dbHandle.fetchMiscAccount(currentMonth, currentYear)
        self.foodLabelTotalValue.setText(str(currFoodTotal))
        self.miscLabelTotalValue.setText(str(currMiscTotal))

    # XXX
    def styleChoiceMethod(self, text):
        self.styleChoice.setText(text)
        print self.comboBox.currentText()
        print self.comboBox.currentText() + "HHHHHH"
        print type(self.comboBox.currentText())
    # XXX

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

        # Get the current month and year
        now = datetime.datetime.now()
        currentMonth = now.strftime('%B')
        currentYear = now.strftime('%Y')

        # Set the value labels
        currFoodTotal = BudgetWidget.dbHandle.fetchFoodAccount(currentMonth, currentYear) + foodValueEnteredByUser
        currMiscTotal = BudgetWidget.dbHandle.fetchMiscAccount(currentMonth, currentYear) + miscValueEnteredByUser
        self.foodLabelTotalValue.setText(str(currFoodTotal))
        self.miscLabelTotalValue.setText(str(currMiscTotal))

        # Update the database with the entered values
        BudgetWidget.dbHandle.insertFoodAccount(currentMonth, currentYear, foodValueEnteredByUser)
        BudgetWidget.dbHandle.insertMiscAccount(currentMonth, currentYear, miscValueEnteredByUser)

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
