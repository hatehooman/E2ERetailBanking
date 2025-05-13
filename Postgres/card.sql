CREATE TABLE card (
	card_id	varchar(50) not null primary key,
	disp_id	varchar(50) not null,
	type varchar(20) not null,
	year integer not null,
	month integer not null,
	day	integer not null,
	fulldate date not null
);