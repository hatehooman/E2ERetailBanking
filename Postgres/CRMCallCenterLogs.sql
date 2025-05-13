CREATE TABLE CRMCallCenterLogs (
	Date_recieved	date not null,
	Complaint_id	varchar(50) null,
	Rand_client	varchar(50) null,
	Phonefinal	varchar(50) not null,
	Vru_line	varchar(50) null,
	Call_id	integer null,
	Priority	integer null,
	Type	varchar(50) null,
	Outcome	varchar(50) null,
	Server	varchar(50) null,
	Ser_start	varchar(50) not null,
	Ser_exit	varchar(50) not null,
	Ser_time	varchar(50) not null
);

