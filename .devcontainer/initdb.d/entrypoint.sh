#!/bin/bash

# start SQL Server
/opt/mssql/bin/sqlservr &

# waiting for SQL Server to start
echo "Waiting for SQL Server to start..."
until sqlcmd -S localhost -U sa -P "$MSSQL_SA_PASSWORD" -N o -Q "SELECT 1" > wait.log 2>&1
do
  sleep 3
done

# initialize the database
echo "Restore the database if it does not exist..."
sqlcmd  -S localhost -i restore.sql -U sa -P "$MSSQL_SA_PASSWORD" -N o > restore.log 2>&1

# add read only user with password from environment variable
echo "Adding read only user..."
echo :setvar TEXT2SQL_PASSWORD "$TEXT2SQL_PASSWORD" > add_readonly_user_replaced.sql
tail -n +4 add_readonly_user.sql >> add_readonly_user_replaced.sql
sqlcmd  -S localhost -i add_readonly_user_replaced.sql -U sa -P "$MSSQL_SA_PASSWORD" -N o > add_readonly_user.log 2>&1


wait