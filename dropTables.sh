#!/bin/bash

# drop all tables
# only used for testing
# Kavin Autar
# 2013/11/07
# Last modified: 2013/11/22
# Version 1.1

user="kav"

psql -d stockmarket -U ${user} -c "DROP TABLE industry CASCADE"
psql -d stockmarket -U ${user} -c "DROP TABLE country CASCADE"
psql -d stockmarket -U ${user} -c "DROP TABLE company CASCADE"
psql -d stockmarket -U ${user} -c "DROP TABLE historic_data CASCADE"
psql -d stockmarket -U ${user} -c "DROP TABLE averages CASCADE"
psql -d stockmarket -U ${user} -c "DROP TABLE change CASCADE"
psql -d stockmarket -U ${user} -c "DROP TABLE eps CASCADE"
psql -d stockmarket -U ${user} -c "DROP TABLE daily CASCADE"
