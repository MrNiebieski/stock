#!/bin/bash

# create tables
# Kavin Autar
# 2013/11/07
#!/bin/bash
psql -d stockmarket -U kav -c "DROP TABLE industry CASCADE"
psql -d stockmarket -U kav -c "DROP TABLE country CASCADE"
psql -d stockmarket -U kav -c "DROP TABLE company CASCADE"
psql -d stockmarket -U kav -c "DROP TABLE historic_data CASCADE"
psql -d stockmarket -U kav -c "DROP TABLE averages CASCADE"
psql -d stockmarket -U kav -c "DROP TABLE change CASCADE"
psql -d stockmarket -U kav -c "DROP TABLE eps CASCADE"
psql -d stockmarket -U kav -c "DROP TABLE daily CASCADE"
