CREATE TABLE c_transaction(
	trans_id	varchar not null primary key,
	account_id	varchar not null,
	type	varchar(50) not null,
	operation	varchar,
	amount	float not null,
	balance	float not null,
	k_symbol	varchar,
	bank	varchar,
	account	varchar,
	year	integer not null,
	month	integer not null,
	day	integer not null,
	fulldate	date not null,
	fulltime	varchar not null,
	fulldatewithtime	varchar not null
);