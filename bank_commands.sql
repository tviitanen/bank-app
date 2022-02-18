PRAGMA foreign_keys = 0;
/* bank_commands.sql
 *
 * Basics of Database Systems
 * 15.2.2022
 *
 * SQL commands for creating tables and inserting data
 *
 * Student No. 00456573 */


-- CREATE TABLES

PRAGMA foreign_keys = 0;

CREATE TABLE "Accounts" (
	"customerID"	INTEGER NOT NULL,
	"accountNumber"	INTEGER NOT NULL,
	FOREIGN KEY("customerID") REFERENCES "Customer"("customerID") ON DELETE CASCADE,
	FOREIGN KEY("accountNumber") REFERENCES "BankAccount"("accountNumber") ON DELETE CASCADE
);
CREATE TABLE "BankAccount" (
	"accountNumber"	TEXT NOT NULL UNIQUE,
	"balance"	INTEGER DEFAULT 0,
	"accountType"	TEXT DEFAULT 'Daily',
	PRIMARY KEY("accountNumber")
	CHECK(length(accountNumber)==18)
);
CREATE TABLE "BankCard" (
	"cardNumber"	INTEGER NOT NULL UNIQUE,
	"customerID"	INTEGER NOT NULL,
	"accountNumber"	TEXT NOT NULL,
	"cardPin"	INTEGER NOT NULL,
	PRIMARY KEY("cardNumber"),
	FOREIGN KEY("customerID") REFERENCES "Customer"("customerID") ON DELETE CASCADE,
	FOREIGN KEY("accountNumber") REFERENCES "BankAccount"("accountNumber") ON DELETE CASCADE
	CHECK(length(cardNumber)==16)
	CHECK(length(customerID)==8)
	CHECK(length(accountNumber)==18)
	CHECK(length(cardPin)==4)
);
CREATE TABLE "Banker" (
	"bankerID"	INTEGER NOT NULL UNIQUE,
	"branchID"	INTEGER NOT NULL,
	"lastname"	TEXT NOT NULL,
	"firstname"	TEXT NOT NULL,
	"email"	TEXT,
	"phoneNumber"	TEXT NOT NULL,
	"pin"		INTEGER NOT NULL,
	PRIMARY KEY("bankerID"),
	FOREIGN KEY("branchID") REFERENCES "Branch"("branchID") ON DELETE CASCADE
	CHECK(length(bankerID)==8)
	CHECK(length(branchID)==5)
	CHECK(length(pin)==4)
);
CREATE TABLE "Branch" (
	"branchID"	INTEGER NOT NULL UNIQUE,
	"location"	TEXT,
	"branchName"	TEXT,
	PRIMARY KEY("branchID")
	CHECK(length(branchID)==5)
);
CREATE TABLE "Customer" (
	"customerID"	INTEGER NOT NULL UNIQUE,
	"bankerID"	INTEGER NOT NULL,
	"lastname"	TEXT NOT NULL,
	"firstname"	TEXT NOT NULL,
	"dateofbirth"	TEXT NOT NULL,
	"pin"	INTEGER NOT NULL,
	PRIMARY KEY("customerID"),
	FOREIGN KEY("bankerID") REFERENCES "Banker"("bankerID") ON DELETE CASCADE
	CHECK(length(customerID)==8)
	CHECK(length(bankerID)==8)
	CHECK(length(pin)==4)
	CHECK(length(dateofbirth)==10)
);
CREATE TABLE "Transactions" (
	"transactionID"	INTEGER NOT NULL UNIQUE,
	"senderAccount"	TEXT NOT NULL,
	"receiverAccount"	TEXT,
	"amount"		INTEGER  NOT NULL,
	PRIMARY KEY("transactionID"),
	FOREIGN KEY("receiverAccount") REFERENCES "BankAccount"("accountNumber"),
	FOREIGN KEY("senderAccount") REFERENCES "BankAccount"("accountNumber"),
	CHECK(length(transactionID)==18)
	CHECK(length(senderAccount)==18)
	CHECK(length(receiverAccount)==18)
);


-- INSERT DATA


INSERT INTO BankAccount(accountNumber, balance, accountType)
VALUES
	('FI5794375395744586', 83498594, 'savings'),
	('FI5794375395744587', 48859, 'use'),
	('FI5794375395744588', 84466, 'use'),
	('FI5794375395744589', 334556547, 'use'),
	('FI5794375395744590', 648574751, 'savings');
INSERT INTO Customer(customerID, bankerID, lastname, firstname, dateofbirth, pin)
VALUES
	(45985947, 85487458, 'Schwarzenegger', 'Arnold', '30.07.1947', 6374),
	(45985948, 85487459, 'Bond', 'James', '11.11.1920', 3784),
	(45985949, 85487460, 'Rambo', 'John', '06.05.1947', 2983),
	(45985950, 85487461, 'Bourne', 'Jason', '13.09.1970', 8935),
	(45985951, 85487462, 'Wayne', 'Bruce', '17.04.1915', 9023);
INSERT INTO BankCard(cardNumber, customerID, accountNumber, cardPin)
VALUES    
	(4785843926376406, 45985947, 'FI5794375395744586', 5434),
	(4785843926376407, 45985948, 'FI5794375395744587', 9489),
	(4785843926376408, 45985949, 'FI5794375395744588', 8778),
	(4785843926376409, 45985950, 'FI5794375395744589', 7284),
	(4785843926376410, 45985951, 'FI5794375395744590', 3489);
INSERT INTO Banker(bankerID, branchID, lastname, firstname, email, phoneNumber, pin)
VALUES
	(85487458, 88676, 'Morgan', 'John', 'john.morgan@jpmorgan.com', '+358408345175', 7843),
	(85487459, 88677, 'Rothschild', 'Charles', 'charles@rothschild.com', '+358408345176', 3784),
	(85487460, 88678, 'Giannini', 'Amadeo', 'amadeo.giannini@bankofamerica.com', '+358408345177', 8434),
	(85487461, 88679, 'Wells', 'Henry', 'henry.wells@wellsfargo.com', '+358408345178', 8398),
	(85487462, 88679, 'Fargo', 'William', 'william.fargo@wellsfargo.com', '+358408345179', 6723);
INSERT INTO Branch(branchID, location, branchName)
VALUES
	(88676, 'New York', 'JP Morgan & Chase'),
	(88677, 'London', 'Rothschild & Co'),
	(88678, 'New York', 'Bank of America'),
	(88679, 'New York', 'Wells Fargo');
INSERT INTO Accounts(customerID, accountNumber)
VALUES
	(45985947, 'FI5794375395744586'),
	(45985948, 'FI5794375395744587'),
	(45985949, 'FI5794375395744588'),
	(45985950, 'FI5794375395744589'),
	(45985951, 'FI5794375395744590');
INSERT INTO Transactions(transactionID, senderAccount, receiverAccount, amount)
VALUES
	(858453141243293758, 'FI5794375395744586', 'FI5794375395744587', 7574),
	(858453141243293759, 'FI5794375395744587', 'FI5794375395744588', 9584),
	(858453141243293760, 'FI5794375395744588', 'FI5794375395744586', 67434),
	(858453141243293761, 'FI5794375395744589', 'FI5794375395744590', 23472),
	(858453141243293762, 'FI5794375395744590', 'FI5794375395744587', 73),
	(858453141243293763, 'FI5794375395744589', 'FI5794375395744588', 1636),
	(858453141243293764, 'FI5794375395744586', 'FI5794375395744590', 7362),
	(858453141243293765, 'FI5794375395744588', 'FI5794375395744587', 2654),
	(858453141243293766, 'FI5794375395744590', 'FI5794375395744586', 273),
	(858453141243293767, 'FI5794375395744587', 'FI5794375395745489', 27448),
	(858453141243293768, 'FI5794375395744589', 'FI5794375395744590', 8389);