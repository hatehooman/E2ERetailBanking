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