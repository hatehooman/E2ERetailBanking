CREATE TABLE CRMEvents(
	Date_received	date not null,
	Product	varchar(50) not null,
	Sub_product	varchar(50),
	Issue	varchar(50) not null,
	Sub_issue	varchar(20),
	Consumer_complaint_narrative 	varchar,
	Tags varchar(50),
	Consumer_consent_provided varchar(20),
	Submitted_via	varchar(20) not null,
	Date_sent_to_company date not null,
	Company_response_to_consumer varchar(50) not null,
	Timely_response	varchar(20) not null,
	Consumer_disputed	varchar(20),
	Complaint_ID	varchar(20) not null primary key,
	Client_ID	varchar(20) not null
);