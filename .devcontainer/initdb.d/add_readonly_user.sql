USE master;
GO

-- Create login for text2sql user with SQL Server authentication if it does not exist
IF NOT EXISTS (SELECT * FROM sys.server_principals WHERE name = 'text2sql')
BEGIN
    CREATE LOGIN text2sql WITH PASSWORD = '6v@lu@t!0n_X';
END
GO

USE AdventureWorks;
GO

-- Create database user linked to the login if it does not exist
IF NOT EXISTS (SELECT * FROM sys.database_principals WHERE name = 'text2sql')
BEGIN
    CREATE USER text2sql FOR LOGIN text2sql;
END
GO

-- Grant read-only access to all data in the database if not already granted
IF NOT EXISTS (
    SELECT * FROM sys.database_role_members
    WHERE member_principal_id = (SELECT principal_id FROM sys.database_principals WHERE name = 'text2sql')
    AND role_principal_id = (SELECT principal_id FROM sys.database_principals WHERE name = 'db_datareader')
)
BEGIN
    ALTER ROLE db_datareader ADD MEMBER text2sql;
END
GO