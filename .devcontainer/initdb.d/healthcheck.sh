#!/bin/bash
sqlcmd -S localhost -U text2sql -P "$TEXT2SQL_PASSWORD" -N o -i healthcheck.sql | grep -q ONLINE
exit $?