-- Run as root: mysql -u root -p < mysql_governance.sql
-- Run AFTER load_to_mysql.py has populated asg_airlines and asg_airlines_restricted.

-- Low-privilege user for Power BI / general analysts: reporting database only.
CREATE USER IF NOT EXISTS 'reporting_reader'@'localhost' IDENTIFIED BY 'ChangeThisPassword!123';
GRANT SELECT ON asg_airlines.* TO 'reporting_reader'@'localhost';
-- No GRANT on asg_airlines_restricted.
FLUSH PRIVILEGES;

-- Verify the boundary:
--   mysql -u reporting_reader -p asg_airlines             -> SELECT COUNT(*) FROM fact_flights;         (succeeds)
--   mysql -u reporting_reader -p asg_airlines_restricted  -> SELECT * FROM secure_booking_pii;           (access denied)

SHOW GRANTS FOR 'reporting_reader'@'localhost';
