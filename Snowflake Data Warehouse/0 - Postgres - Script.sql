/*===================Account==================*/

CREATE TYPE account_frequency_enum AS ENUM (
	'Issuance After Transaction',
	'Monthly Issuance',
	'Weekly Issuance'
);

CREATE TABLE account (
	account_id varchar(20) not null primary key,
	district_id integer not null,
	frequency account_frequency_enum not null,
	parseddate date not null,
	year integer not null,
	month integer not null,
	day integer not null
);

/*====================Card====================*/
CREATE TYPE card_type_enum AS ENUM(
	'VISA Signature',
	'VISA Standard',
	'VISA Infinite'
);

CREATE TABLE card (
	card_id	varchar(50) not null primary key,
	disp_id	varchar(50) not null,
	"type" card_type_enum not null,
	"year" integer not null,
	"month" integer not null,
	"day"	integer not null,
	fulldate date not null
);


/*===================Client===================*/
CREATE TABLE client (
	client_id varchar not null primary key,
	sex	varchar not null,
	fulldate date not null,
	"day"	integer not null,
	"month"	integer not null,
	"year"	integer not null,
	age		integer not null,
	social	varchar not null,
	"first"	varchar not null,
	middle	varchar not null,
	"last"	varchar not null,
	phone	varchar not null,
	email	varchar not null,
	address_1	varchar not null,
	address_2	varchar,
	city	varchar not null,
	"state"	varchar not null,
	zipcode	int not null,
	district_id	integer not null
);






/*===================Disposition===================*/
CREATE TYPE disposition_type_enum AS ENUM (
	'Owner',
	'User'
);
CREATE TABLE disposition (
	disp_id	varchar(20) not null primary key,
	client_id	varchar(20) not null,
	account_id	varchar(20) not null,
	"type"	disposition_type_enum not null
);


/*===================District===================*/
CREATE TABLE district (
	district_id	integer not null primary key, 
	city	varchar(50) not null, 
	state_name	varchar(50) not null, 
	state_abbrev varchar(50) not null, 
	region	varchar(50) not null, 
	division varchar(50) not null
);

/*===================Loan===================*/
CREATE TABLE loan (
	loan_id	varchar(20) not null primary key,
	account_id	varchar(20) not null,
	amount	float not null,
	duration	integer not null,
	payments	integer not null,
	status	varchar(5) not null,
	"year"	integer not null,
	"month"	integer not null,
	"day"	integer not null,
	fulldate	date not null,
	"location"	integer not null,
	purpose	varchar(20) not null
);



/*===================Order===================*/
CREATE TABLE "order"(
	order_id	integer not null primary key,
	account_id	varchar(50) not null,
	bank_to	varchar(50) not null,
	account_to	integer not null,
	amount	float not null,
	k_symbol	varchar(50)
);



/*===================Transaction===================*/
CREATE TABLE transaction(
	"index" int,
	trans_id	varchar(50) not null primary key,
	account_id	varchar(50) not null,
	"type"	varchar(50) not null,
	operation	varchar(50),
	amount	float not null,
	balance	float not null,
	k_symbol	varchar(50),
	bank	varchar(50),
	account	varchar(50),
	"year"	integer not null,
	"month"	integer not null,
	"day"	integer not null,
	fulldate	date not null,
	fulltime	varchar(50) not null,
	fulldatewithtime	varchar(50) not null
);
/*===================Call Center Logs===================*/
CREATE TABLE CRMCallCenterLogs (
	Date_recieved	date not null,
	Complaint_id	varchar(50) null,
	Rand_client	varchar(50) null,
	Phonefinal	varchar(50) not null,
	Vru_line	varchar(50) null,
	Call_id	int null,
	Priority	integer null,
	"Type"	varchar(50) null,
	Outcome	varchar(50) null,
	"Server"	varchar(50) null,
	Ser_start	varchar(50) not null,
	Ser_exit	varchar(50) not null,
	Ser_time	varchar(50) not null
);
/*CRM Reviews*/
CREATE TABLE CRMReviews (
	Date	date not null,
	Stars	integer not null,
	Reviews	varchar,
	Product	varchar(50) not null,
	district_id	integer not null
);
/*CRM Events*/
CREATE TABLE CRMEvents(
	"Date received"	date not null,
	"Product"	varchar(50) not null,
	"Sub-product"	varchar(50),
	"Issue"	varchar(50) not null,
	"Sub-issue"	varchar(20),
	"Consumer complaint narrative" 	varchar,
	"Tags" varchar(50),
	"Consumer consent provided" varchar(20),
	"Submitted via"	varchar(20) not null,
	"Date sent to company" date not null,
	"Company response to consumer" varchar(50) not null,
	"Timely response"	varchar(20) not null,
	"Consumer disputed"	varchar(20),
	"Complaint ID"	varchar(20) not null primary key,
	Client_ID	varchar(20) not null
);
/*=============================================CONSTRAINT============================================================*/
ALTER TABLE
	transaction
ADD
	FOREIGN KEY (account_id) REFERENCES account(account_id) on delete cascade;

ALTER TABLE
	loan
ADD
	FOREIGN KEY (account_id) references account(account_id) on delete cascade;

ALTER TABLE
	transaction
ADD
	FOREIGN KEY (account_id) REFERENCES account(account_id) on delete cascade;

ALTER TABLE
	CRMEvents
ADD
	FOREIGN KEY (Client_ID) REFERENCES client(client_id) on delete cascade;

ALTER TABLE
	CRMCallCenterLogs
ADD
	FOREIGN KEY (Complaint_id) REFERENCES CRMEvents("Complaint ID") on delete cascade;

ALTER TABLE
	"order"
ADD
	FOREIGN KEY (account_id) references account(account_id) on delete cascade;

ALTER TABLE
	account
ADD
	foreign key(district_id) references district(district_id) on delete cascade;

ALTER TABLE
	card
ADD
	foreign key(disp_id) references disposition(disp_id) on delete cascade;

ALTER TABLE
	disposition
ADD
	foreign key (client_id) references client(client_id) on delete cascade;


ALTER TABLE
	client
ADD
	foreign key (district_id) references district(district_id) on delete cascade;

ALTER TABLE
	CRMReviews
ADD
	foreign key (district_id) references district(district_id) on delete cascade;


/*===========================================Sample for test=================================================*/
/*=================== Account ==================*/
INSERT INTO account (account_id, district_id, frequency, parseddate, year, month, day)
VALUES
('A00000001', 1, 'Monthly Issuance', '2024-06-25', 2024, 6, 25),
('A00000002', 2, 'Weekly Issuance', '2024-06-24', 2024, 6, 24);

/*==================== Card ====================*/
INSERT INTO card (card_id, disp_id, "type", "year", "month", "day", fulldate)
VALUES
('C00000001', 'D00000001', 'VISA Signature', 2024, 6, 25, '2024-06-25'),
('C00000002', 'D00000002', 'VISA Standard', 2024, 6, 24, '2024-06-24');

/*=================== Client ===================*/
INSERT INTO client (client_id, sex, fulldate, "day", "month", "year", age, social, "first", middle, "last", phone, email, address_1, address_2, city, "state", zipcode, district_id)
VALUES
('CL00000001', 'Male', '2024-06-25', 25, 6, 2024, 30, '123-45-6789', 'John', 'M', 'Doe', '123-456-7890', 'john.doe@example.com', '123 Main St', 'Apt 4B', 'Springfield', 'IL', 62701, 1),
('CL00000002', 'Female', '2024-06-24', 24, 6, 2024, 28, '987-65-4321', 'Jane', 'A', 'Smith', '098-765-4321', 'jane.smith@example.com', '456 Elm St', null, 'Shelbyville', 'IL', 62702, 2);

/*=================== Disposition ===============*/
INSERT INTO disposition (disp_id, client_id, account_id, "type")
VALUES
('D00000001', 'CL00000001', 'A00000001', 'Owner'),
('D00000002', 'CL00000002', 'A00000002', 'User');

/*=================== District ==================*/
INSERT INTO district (district_id, city, state_name, state_abbrev, region, division)
VALUES
(1, 'Springfield', 'Illinois', 'IL', 'Midwest', 'East North Central'),
(2, 'Shelbyville', 'Illinois', 'IL', 'Midwest', 'East North Central');

/*=================== Loan =====================*/
INSERT INTO loan (loan_id, account_id, amount, duration, payments, status, "year", "month", "day", fulldate, "location", purpose)
VALUES
('L00000001', 'A00000001', 10000.0, 24, 500, 'Approved', 2024, 6, 25, '2024-06-25', 1, 'Car'),
('L00000002', 'A00000002', 5000.0, 12, 450, 'Rejected', 2024, 6, 24, '2024-06-24', 2, 'Personal');

/*=================== Order ====================*/
INSERT INTO "order" (order_id, account_id, bank_to, account_to, amount, k_symbol)
VALUES
(1, 'A00000001', 'Bank A', 123456789, 1000.0, 'Payment'),
(2, 'A00000002', 'Bank B', 987654321, 500.0, 'Deposit');

/*=================== Transaction ==============*/
INSERT INTO transaction ("index", trans_id, account_id, "type", operation, amount, balance, k_symbol, bank, account, "year", "month", "day", fulldate, fulltime, fulldatewithtime)
VALUES
(1, 'T00000001', 'A00000001', 'Credit', 'Online', 1000.0, 2000.0, 'Deposit', 'Bank A', '123456789', 2024, 6, 25, '2024-06-25', '12:00:00', '2024-06-25 12:00:00'),
(2, 'T00000002', 'A00000002', 'Debit', 'ATM', 500.0, 1500.0, 'Withdrawal', 'Bank B', '987654321', 2024, 6, 24, '2024-06-24', '15:00:00', '2024-06-24 15:00:00');

/*================= CRM Call Center Logs =======*/
INSERT INTO CRMCallCenterLogs (Date_recieved, Complaint_id, Rand_client, Phonefinal, Vru_line, Call_id, Priority, "Type", Outcome, "Server", Ser_start, Ser_exit, Ser_time)
VALUES
('2024-06-25', 'CMP0001', 'CL00000001', '123-456-7890', 'VRU1', 1, 1, 'Complaint', 'Resolved', 'Server1', '12:00', '12:30', '30 mins'),
('2024-06-24', 'CMP0002', 'CL00000002', '098-765-4321', 'VRU2', 2, 2, 'Query', 'Pending', 'Server2', '13:00', '13:20', '20 mins');

/*================= CRM Reviews ================*/
INSERT INTO CRMReviews (Date, Stars, Reviews, Product, district_id)
VALUES
('2024-06-25', 5, 'Great service!', 'Credit Card', 1),
('2024-06-24', 3, 'Average experience.', 'Loan', 2);

/*================= CRM Events =================*/
INSERT INTO CRMEvents ("Date received", "Product", "Sub-product", "Issue", "Sub-issue", "Consumer complaint narrative", "Tags", "Consumer consent provided", "Submitted via", "Date sent to company", "Company response to consumer", "Timely response", "Consumer disputed", "Complaint ID", Client_ID)
VALUES
('2024-06-25', 'Credit Card', 'Rewards', 'Billing error', 'Incorrect charge', 'I was charged incorrectly for my rewards points.', 'Rewards', 'Yes', 'Web', '2024-06-25', 'Corrected', 'Yes', 'No', 'CMP0001', 'CL00000001'),
('2024-06-24', 'Loan', 'Personal Loan', 'Late payment', 'Interest charge', 'I was charged a late fee even though I paid on time.', 'Loan', 'No', 'Email', '2024-06-24', 'Pending', 'No', 'Yes', 'CMP0002', 'CL00000002');
