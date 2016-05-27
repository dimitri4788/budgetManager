#!/usr/bin/python #FIXME change this
# -*- coding: utf-8 -*-

import datetime
import sys

from PyQt4 import QtGui

from database import Datastore
from csvgenerator import *
from pdfgenerator import *


#TODO: Add comments everywhere
class BudgetWidget(QtGui.QWidget):
    """TODO """

    # TODO I am here
    # First get the handle to Datastore
    dbHandle = Datastore()
    dbHandle.connect()

    def __init__(self):
        # First construct QWidget
        super(BudgetWidget, self).__init__()

        # Create labels
        self.header = QtGui.QLabel("Budget Manager", self)
        now = datetime.datetime.now()
        self.currentDate = QtGui.QLabel(now.strftime('%B %Y'), self)
        self.currentTotal = QtGui.QLabel("Current Total", self)
        self.foodLabel = QtGui.QLabel("Food", self)
        self.miscLabel = QtGui.QLabel("Miscellaneous", self)
        self.foodLabelTotalValue = QtGui.QLabel("000000000000000000", self)
        self.miscLabelTotalValue = QtGui.QLabel("000000000000000000", self)
        #self.miscLabel.setStyleSheet('color: yellow')

        # Create line-edits
        self.foodLineedit = QtGui.QLineEdit(self)
        self.miscLineedit = QtGui.QLineEdit(self)

        # Create push-buttons
        self.submitButton = QtGui.QPushButton('Submit', self)
        self.csvButton = QtGui.QPushButton('Generate CSV', self)
        self.pdfButton = QtGui.QPushButton('Generate PDF', self)

        # Set labels positions
        self.header.move(200, 20)
        self.currentDate.move(200, 40)
        self.currentTotal.move(300, 60)
        self.foodLabel.move(5, 80)
        self.miscLabel.move(5, 100)
        self.foodLabelTotalValue.move(330, 80)
        self.miscLabelTotalValue.move(330, 100)

        # Set line-edits positions and size
        self.foodLineedit.move(90, 80)
        self.foodLineedit.resize(90, 20)
        self.miscLineedit.move(90, 100)
        self.miscLineedit.resize(90, 20)

        # Set position of submitButton and the action associated with it
        self.submitButton.move(100, 200)
        self.submitButton.clicked.connect(self.submitButtonClicked)
        self.submitButton.setStyleSheet("background-color: red; border-style: outset; border-width: 2px; border-radius: 10px; border-color: beige; font: bold 14px; min-width: 10em; padding: 6px");

        # Set position of csvButton and the action associated with it
        self.csvButton.move(100, 250)
        self.csvButton.clicked.connect(self.csvButtonClicked)
        self.csvButton.setStyleSheet("background-color: green; border-style: outset; border-width: 2px; border-radius: 10px; border-color: beige; font: bold 14px; min-width: 10em; padding: 6px");

        # Set position of pdfButton and the action associated with it
        self.pdfButton.move(100, 300)
        self.pdfButton.clicked.connect(self.pdfButtonClicked)
        self.pdfButton.setStyleSheet("background-color: green; border-style: outset; border-width: 2px; border-radius: 10px; border-color: beige; font: bold 14px; min-width: 10em; padding: 6px");

        # Set app window size and title
        self.setGeometry(300, 300, 550, 350)
        self.setWindowTitle('Budget Manager')
        self.show()

        # Fill the line-edits with the amount for food and misc
        currentMonth = now.strftime('%B')
        currentYear = now.strftime('%Y')
        currFoodTotal = BudgetWidget.dbHandle.fetchFoodAccount(currentMonth, currentYear)
        currMiscTotal = BudgetWidget.dbHandle.fetchMiscAccount(currentMonth, currentYear)
        print "currFoodTotal", currFoodTotal
        print "currMiscTotal", currMiscTotal
        self.foodLabelTotalValue.setText(str(currFoodTotal))
        self.miscLabelTotalValue.setText(str(currMiscTotal))
        #BudgetWidget.dbHandle.insertFoodAccount(currentMonth, currentYear, currFoodTotal)
        #BudgetWidget.dbHandle.insertMiscAccount(currentMonth, currentYear, currMiscTotal)
        #BudgetWidget.dbHandle.insertFoodAccount(currentMonth, currentYear, 33)
        #BudgetWidget.dbHandle.insertMiscAccount(currentMonth, currentYear, 44)


    def submitButtonClicked(self):
        """TODO """
        #print self.foodLineedit.text()
        #print self.miscLineedit.text()
        now = datetime.datetime.now()
        currentMonth = now.strftime('%B')
        currentYear = now.strftime('%Y')
        BudgetWidget.dbHandle.insertFoodAccount(currentMonth, currentYear, 33)
        BudgetWidget.dbHandle.insertMiscAccount(currentMonth, currentYear, 44)
        #print "curr food: ", BudgetWidget.dbHandle.fetchFoodAccount(currentMonth, currentYear)
        #print "curr misc: ", BudgetWidget.dbHandle.fetchMiscAccount(currentMonth, currentYear)
        #print "deep"

    def csvButtonClicked(self):
        genCSV(BudgetWidget.dbHandle)

    def pdfButtonClicked(self):
        print "Hi Deep"

def main():
    """This function is where the budget app starts."""

    app = QtGui.QApplication(sys.argv)
    ex = BudgetWidget()
    sys.exit(app.exec_())


# Execute only if run as a script
if __name__ == "__main__":
    main()
