CREATE TABLE district (
	district_id	integer not null primary key, 
	city	varchar(50) not null, 
	state_name	varchar(50) not null, 
	state_abbrev varchar(50) not null, 
	region	varchar(50) not null, 
	division varchar(50) not null
);