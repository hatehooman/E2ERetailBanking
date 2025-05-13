CREATE TABLE account (
	account_id varchar(50) not null primary key,
	district_id integer not null,
	frequency varchar(50) not null,
	parseddate date not null,
	year integer not null,
	month integer not null,
	day integer not null
);
