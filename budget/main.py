#!/usr/bin/python #FIXME change this
# -*- coding: utf-8 -*-

import datetime
import sys

from PyQt4 import QtGui


class BudgetWidget(QtGui.QWidget):
    """TODO """

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
        #self.miscLabel.setStyleSheet('color: yellow')


        # Create line-edits
        self.foodLineedit = QtGui.QLineEdit(self)
        self.miscLineedit = QtGui.QLineEdit(self)

        # Create push-buttons
        self.submitButton = QtGui.QPushButton('Submit', self)

        # Set labels positions
        self.header.move(200, 20)
        self.currentDate.move(200, 40)
        self.currentTotal.move(300, 60)
        self.foodLabel.move(5, 80)
        self.miscLabel.move(5, 100)

        # Set line-edits positions and size
        self.foodLineedit.move(90, 80)
        self.foodLineedit.resize(90, 20)
        self.miscLineedit.move(90, 100)
        self.miscLineedit.resize(90, 20)

        self.submitButton.move(100, 200)
        self.submitButton.clicked.connect(self.on_pushButtonOK_clicked)
        self.submitButton.setStyleSheet("background-color: red; border-style: outset; border-width: 2px; border-radius: 10px; border-color: beige; font: bold 14px; min-width: 10em; padding: 6px");

        self.setGeometry(300, 300, 550, 350)
        self.setWindowTitle('Budget Manager')
        self.show()

    def on_pushButtonOK_clicked(self):
        """TODO """
        print self.foodLineedit.text()
        print self.miscLineedit.text()
        print "deep"


def main():
    """This function is where the budget app starts."""

    app = QtGui.QApplication(sys.argv)
    ex = BudgetWidget()
    sys.exit(app.exec_())


# Execute only if run as a script
if __name__ == "__main__":
    main()


#TODO: Add comments everywhere
