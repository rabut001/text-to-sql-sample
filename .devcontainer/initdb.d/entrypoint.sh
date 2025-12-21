#!/bin/bash

# start SQL Server
/opt/mssql/bin/sqlservr &

# waiting for SQL Server to start
echo "Waiting for SQL Server to start..."
until sqlcmd -S localhost -U sa -P $MSSQL_SA_PASSWORD -N o -Q "SELECT 1" &> /dev/null
do
  sleep 3
done

# initialize the database
echo "Restore the database if it does not exist..."
sqlcmd  -S localhost -i restore.sql -U sa -P $MSSQL_SA_PASSWORD -N o > restore.log

wait