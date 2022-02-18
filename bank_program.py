###########################################################
## bank_program.py                                  
##
## PROGRAM TO BROWSE BANK DATA
##
## Basics of Database Systems
## 15.2.2022
## 
## Student No. 00456573
##
## *** IMPORTANT ****
## UserID's and pin-codes to operate program can be found from
## users.text and from report.docx
##
###########################################################


import sqlite3
from bokeh.io import output_file, show
from bokeh.plotting import figure, save

db = sqlite3.connect('bank_database.sqlite')
db.row_factory = sqlite3.Row
cur = db.cursor()

def initializeDB():
    try:
        f = open("sqlcommands.sql", "r")
        commandstring = ""
        for line in f.readlines():
            commandstring+=line
        cur.executescript(commandstring)
    except sqlite3.OperationalError:
        print("Database exists, skip initialization")
    except:
        print("No SQL file to be used for initialization") 
    return None

def main():
    initializeDB()
    ID, userGroup = identificate()
    if userGroup == "customer":
        customerMenu(ID)
    elif userGroup == "banker":
        bankerMenu(ID)

    db.close()        
    return None

# identificate user with user id and pin code

def identificate():
    print("\nLog in:")
    print("1: As banker")
    print("2: As customer")
    userInput = input("Your choice: ")
    if (userInput == "1"):
        try:
            ID = int(input("Give your banker ID: "))
            pin = int(input("Give your PIN-code: "))
            cur.execute("SELECT * FROM Banker WHERE BankerID=(?)", (ID,))
            row = cur.fetchone()
            pinCode = row['pin']
            if pinCode == pin:
                print("Logged in as", row['firstname'], row['lastname'])
                user = "banker"
                return ID, user
        except:
            print("Wrong banker ID or PIN-code.")
            identificate()
    elif (userInput == "2"):
        try:
            ID = int(input("Give your customer ID: "))
            pin = int(input("Give your PIN-code: "))
            cur.execute("SELECT * FROM Customer WHERE CustomerID=(?)", (ID,))
            row = cur.fetchone()
            pinCode = row['pin']
            if pinCode == pin:
                print("Logged in as", row['firstname'], row['lastname'])
                user = "customer"
                return ID, user
        except:
            print("Wrong customer ID or PIN-code.")
            identificate()
    else:
        print("Unknown choise.")
        identificate()

def customerMenu(ID):
    while True:
        print("\nMenu options:")
        print("1: Print transactions")
        print("2: Print accounts")
        print("3: Print cards")
        print("4: Print banker information")
        print("5: Withdraw money from account")
        print("0: Quit")
        userInput = input("What do you want to do: ")
        if userInput == "1":
            printTransactions(ID)
        if userInput == "2":
            printAccounts(ID)
        if userInput == "3":
            printCards(ID)
        if userInput == "4":
            printBanker(ID)
        if userInput == "5":
            withdraw(ID)
        if userInput == "0":
            print("Ending software...")
            break
    return None

def bankerMenu(ID):
    while True:
        print("\nMenu options:")
        print("1: Print Customers")
        print("2: Print accounts of a customer")
        print("3: Visualize account balances")
        print("0: Quit")
        userInput = input("What do you want to do: ")
        if userInput == "1":
            printCustomers(ID)
        if userInput == "2":
            printCustomersAccounts(ID)
        if userInput == "3":
            visualize()
        if userInput == "0":
            print("Ending software...")
            break
    return None

#####################
# CUSTOMER OPTIONS  #
#####################


def printTransactions(ID):
    print("\nPrinting transactions")
    cur.execute('SELECT * FROM Transactions INNER JOIN Accounts ON Transactions.senderAccount = Accounts.accountNumber WHERE Accounts.customerID = (?)', (ID,))
    results = cur.fetchall()
    print("\tTransactionID\t\t Sender account\t\t Receiver account\t Amount")
    for row in results:
        print("\t" + str(row['transactionID']), "\t", row['senderAccount'], "\t", row['receiverAccount'], "\t", str(row['amount']) + "€")
    return None

def printAccounts(ID):
    print("\nPrinting accounts")
    cur.execute("SELECT * FROM BankAccount INNER JOIN Accounts ON BankAccount.accountNumber = Accounts.accountNumber WHERE Accounts.customerID = (?)", (ID,))
    results = cur.fetchall()
    print(" \t Account number\t\t Balance\t Account type")
    for row in results:
        print("\t", row['accountNumber'], "\t", str(row['balance']) + "€ \t", row['accountType'])
    return None

def printCards(ID):
    print("\nPrinting bank cards")
    cur.execute("SELECT * FROM BankCard WHERE customerID = (?)", (ID,))
    results = cur.fetchall()
    print("\t Card number \t\t Account number")
    for row in results:
        print("\t", row['cardNumber'], "\t", row['accountNumber'])
    return None

def printBanker(ID):
    print("\nPrinting banker information")
    cur.execute("SELECT * FROM Banker INNER JOIN Customer ON Banker.bankerID = Customer.bankerID WHERE Customer.customerID = (?)", (ID,))
    results = cur.fetchall()
    print("\t Banker name\t Email\t\t\t\t Phone number")
    for row in results:
        print("\t", row['firstname'], row['lastname'], "\t", row['email'], "\t", row['phoneNumber'])

    return None

def withdraw(ID):
    print("\nWitdraw money from account")
    cur.execute("SELECT * FROM BankAccount INNER JOIN Accounts ON BankAccount.accountNumber = Accounts.accountNumber WHERE Accounts.customerID = (?)", (ID,))
    results = cur.fetchall()
    print(" \t Account number\t\t Balance\t Account type")
    for row in results:
        print("\t", row['accountNumber'], "\t", str(row['balance']) + "€ \t", row['accountType'])
    try:
        account = str(input("\nGive account you want to withdraw from: "))
        amount = int(input("Give amount you want to withdraw: "))
        account = str(row['accountNumber'])
        new_balance = int(row['balance']) - int(amount)
        cur.execute("UPDATE BankAccount SET balance = (?) WHERE BankAccount.accountNumber = (SELECT Accounts.accountNumber FROM Accounts WHERE customerID = (?))", (new_balance, ID,))
        cur.execute("INSERT INTO Transactions (senderAccount, receiverAccount, amount) VALUES (?, NULL, ?)", (account, amount))
        print("\n €€€€€    WHITDRAWN", amount, "euros    €€€€€")
        db.commit()
    except:
        print("Something went wrong")
    return None
#####################
# BANKER OPTIONS  #
#####################

def printCustomers(ID):
    print("\nPrinting customer information")
    cur.execute("SELECT * FROM Customer INNER JOIN Banker ON Customer.bankerID = Banker.bankerID WHERE Banker.bankerID = (?)", (ID,))
    results = cur.fetchall()
    for row in results:
        print("Name:", row['firstname'], row['lastname'])
        print("CustomerID:", row['customerID'])
        print("Date of birth:", row['dateOfBirth'])
    return None

def printCustomersAccounts(ID):
    try:
        customerID = int(input("\nGive ID of the customer: "))
        cur.execute("SELECT * FROM Customer WHERE Customer.customerID = (?)", (customerID,))
        bankerID = cur.fetchone()
        bankerID = bankerID["bankerID"]
        # check if bankers ID and bankerID found from customers data matches
        if bankerID == ID:
            cur.execute("SELECT Customer.lastname, Customer.firstname, BankAccount.accountNumber, BankAccount.balance FROM BankAccount INNER JOIN Accounts ON BankAccount.accountNumber = Accounts.accountNumber INNER JOIN Customer ON Accounts.customerID = Customer.customerID WHERE Customer.customerID = (?)", (customerID,))
            results = cur.fetchall()
            for row in results:
                print("Name:\t", row['firstname'], row['lastname'])
                print("Account number:\t", row['accountNumber'])
                print("Balance:\t", row['balance'], "€")
    except:
        print("User is not your client or doesn't exist.")
    return None

def visualize():
    accounts = []
    balances = []
    i = 1
    output_file("balances.html")
    cur.execute("SELECT balance FROM BankAccount")
    results = cur.fetchall()
    for row in results:
        balances.append(row['balance'])
        accounts.append("Customer" + str(i))
        i +=1
        
    p = figure(x_range=accounts, height=350, title="Account balances",
           toolbar_location=None, tools="")

    p.vbar(x=accounts, top=balances, width=0.9)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    show(p)
    return None

main()
