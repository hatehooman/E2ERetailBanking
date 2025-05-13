CREATE TABLE loan (
	loan_id	varchar(20) not null primary key,
	account_id	varchar(20) not null,
	amount	integer not null,
	duration	integer not null,
	payments	integer not null,
	status	varchar(20) not null,
	year	integer not null,
	month	integer not null,
	day	integer not null,
	fulldate	date not null,
	location	integer not null,
	purpose	varchar(20) not null
);