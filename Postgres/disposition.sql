CREATE TABLE disposition (
	disp_id	varchar(20) not null primary key,
	client_id	varchar(20) not null,
	account_id	varchar(20) not null,
	type	varchar(20) not null
);