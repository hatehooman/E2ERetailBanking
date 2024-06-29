CREATE TABLE transaction(
	index int,
	trans_id	varchar(50) not null primary key,
	account_id	varchar(50) not null,
	type	varchar(50) not null,
	operation	varchar(50),
	amount	float not null,
	balance	float not null,
	k_symbol	varchar(50),
	bank	varchar(50),
	account	varchar(50),
	year	integer not null,
	month	integer not null,
	day	integer not null,
	fulldate	date not null,
	fulltime	varchar(50) not null,
	fulldatewithtime	varchar(50) not null
);