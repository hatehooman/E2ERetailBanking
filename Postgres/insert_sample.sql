/*===========================================Sample for test=================================================*/
/*=================== District ==================*/
INSERT INTO district (district_id, city, state_name, state_abbrev, region, division)
VALUES
(1, 'Springfield', 'Illinois', 'IL', 'Midwest', 'East North Central'),
(2, 'Shelbyville', 'Illinois', 'IL', 'Midwest', 'East North Central');


/*=================== Account ==================*/
INSERT INTO account (account_id, district_id, frequency, parseddate, year, month, day)
VALUES
('A00000001', 1, 'Monthly Issuance', '2024-06-25', 2024, 6, 25),
('A00000002', 2, 'Weekly Issuance', '2024-06-24', 2024, 6, 24);
/*=================== Client ===================*/
INSERT INTO client (client_id, sex, fulldate, day, month, year, age, social, first, middle, last, phone, email, address_1, address_2, city, state, zipcode, district_id)
VALUES
('CL00000001', 'Male', '2024-06-25', 25, 6, 2024, 30, '123-45-6789', 'John', 'M', 'Doe', '123-456-7890', 'john.doe@example.com', '123 Main St', 'Apt 4B', 'Springfield', 'IL', 62701, 1),
('CL00000002', 'Female', '2024-06-24', 24, 6, 2024, 28, '987-65-4321', 'Jane', 'A', 'Smith', '098-765-4321', 'jane.smith@example.com', '456 Elm St', null, 'Shelbyville', 'IL', 62702, 2);

/*================= CRM Reviews ================*/
INSERT INTO CRMReviews (Date, Stars, Reviews, Product, district_id)
VALUES
('2024-06-25', 5, 'Great service!', 'Credit Card', 1),
('2024-06-24', 3, 'Average experience.', 'Loan', 2);

/*=================== Loan =====================*/
INSERT INTO loan (loan_id, account_id, amount, duration, payments, status, year, month, day, fulldate, location, purpose)
VALUES
('L00000001', 'A00000001', 10000.0, 24, 500, 'A', 2024, 6, 25, '2024-06-25', 1, 'Car'),
('L00000002', 'A00000002', 5000.0, 12, 450, 'C', 2024, 6, 24, '2024-06-24', 2, 'Personal');

/*=================== Order ====================*/
INSERT INTO c_order (order_id, account_id, bank_to, account_to, amount, k_symbol)
VALUES
(3, 'A00000001', 'Bank A', 123456789, 1000.0, 'Payment'),
(2, 'A00000002', 'Bank B', 987654321, 500.0, 'Deposit');

/*=================== Transaction ==============*/
INSERT INTO transaction ("index", trans_id, account_id, "type", operation, amount, balance, k_symbol, bank, account, year, month, day, fulldate, fulltime, fulldatewithtime)
VALUES
(1, 'T00000001', 'A00000001', 'Credit', 'Online', 1000.0, 2000.0, 'Deposit', 'Bank A', '123456789', 2024, 6, 25, '2024-06-25', '12:00:00', '2024-06-25 12:00:00'),
(2, 'T00000002', 'A00000002', 'Debit', 'ATM', 500.0, 1500.0, 'Withdrawal', 'Bank B', '987654321', 2024, 6, 24, '2024-06-24', '15:00:00', '2024-06-24 15:00:00');



/*=================== Disposition ===============*/
INSERT INTO disposition (disp_id, client_id, account_id, type)
VALUES
('D00000001', 'CL00000001', 'A00000001', 'Owner'),
('D00000002', 'CL00000002', 'A00000002', 'User');


/*==================== Card ====================*/
INSERT INTO card (card_id, disp_id, type, year, month, day, fulldate)
VALUES
('C00000001', 'D00000001', 'VISA Signature', 2024, 6, 25, '2024-06-25'),
('C00000002', 'D00000002', 'VISA Standard', 2024, 6, 24, '2024-06-24');


/*================= CRM Events =================*/
INSERT INTO CRMEvents (Date_received, Product, Sub_product, Issue, Sub_issue, Consumer_complaint_narrative, Tags, Consumer_consent_provided, Submitted_via, Date_sent_to_company, Company_response_to_consumer, Timely_response, Consumer_disputed, Complaint_ID, Client_ID)
VALUES
('2024-06-25', 'Credit Card', 'Rewards', 'Billing error', 'Incorrect charge', 'I was charged incorrectly for my rewards points.', 'Rewards', 'Yes', 'Web', '2024-06-25', 'Corrected', 'Yes', 'No', 'CMP0001', 'CL00000001'),
('2024-06-24', 'Loan', 'Personal Loan', 'Late payment', 'Interest charge', 'I was charged a late fee even though I paid on time.', 'Loan', 'No', 'Email', '2024-06-24', 'Pending', 'No', 'Yes', 'CMP0002', 'CL00000002');

/*================= CRM Call Center Logs =======*/
INSERT INTO CRMCallCenterLogs
VALUES
('2024-06-25', 'CMP0001', 'CL00000001', '123-456-7890', 'VRU1', 1, 1, 'Complaint', 'Resolved', 'Server1', '12:00', '12:30', '30 mins'),
('2024-06-24', 'CMP0002', 'CL00000002', '098-765-4321', 'VRU2', 2, 2, 'Query', 'Pending', 'Server2', '13:00', '13:20', '20 mins');