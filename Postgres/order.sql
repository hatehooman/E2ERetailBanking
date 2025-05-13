CREATE TABLE c_order(
	order_id	integer not null primary key,
	account_id	varchar(50) not null,
	bank_to	varchar(50) not null,
	account_to	integer not null,
	amount	float not null,
	k_symbol	varchar(50)
);
