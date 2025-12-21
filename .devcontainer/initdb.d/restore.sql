USE [master];
GO

IF DB_ID(N'AdventureWorks') IS NULL
BEGIN
	RESTORE DATABASE [AdventureWorks]
	FROM DISK = '/docker-entrypoint-initdb.d/AdventureWorks2022.bak'
	WITH
		MOVE 'AdventureWorks2022' TO '/var/opt/mssql/data/AdventureWorks.mdf',
		MOVE 'AdventureWorks2022_log' TO '/var/opt/mssql/log/AdventureWorks_log.ldf',
		FILE = 1,
		NOUNLOAD,
		STATS = 5;
END
ELSE
BEGIN
    PRINT 'Database [AdventureWorks] already exists. Skipping restore.';
END
GO