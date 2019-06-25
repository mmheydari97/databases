DELIMITER $$
create trigger add_access_log after insert on Role
for each row
begin
insert into accessLogs values(new.customerNumber, new.role, current_timestamp());
end$$
DELIMITER ;
