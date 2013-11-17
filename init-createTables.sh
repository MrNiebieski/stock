#!/bin/bash

# create tables
# Kavin Autar
# 2013/11/07

user="kav"

createIndustry="CREATE TABLE industry (
id      SERIAL NOT NULL,
name    text UNIQUE NOT NULL,
PRIMARY KEY (id)
);"

createCountry="CREATE TABLE country (
id	SERIAL NOT NULL,
name	text,
suffix	text,
PRIMARY KEY (id)
);"

createCompany="CREATE TABLE company (
code		text,
name		text,
industry_id	integer,
country_id	integer,
PRIMARY KEY (code),
FOREIGN KEY (industry_id) REFERENCES industry(id),
FOREIGN KEY (country_id) REFERENCES country(id)
);"

createHistoric="CREATE TABLE historic_data (
date		date,
code		text,
high		decimal,
low	    	decimal,
open		decimal,
close		decimal,
volume		decimal,
adj_volume	decimal,
PRIMARY KEY (date, code),
FOREIGN KEY (code) REFERENCES company(code)
);"

createAverages="CREATE TABLE averages (
date        			        date,
code	                   		text,
AverageDailyVolume              bigint,
TwoHundreddayMovingAverage      decimal,
FiftydayMovingAverage           decimal,
PRIMARY KEY (date, code),
FOREIGN KEY (code) REFERENCES company(code)
);"

createChange="CREATE TABLE change (
date					        date,
code           					text,
Change                                          decimal,
ChangeFromFiftydayMovingAverage                 decimal,
ChangeFromTwoHundreddayMovingAverage            decimal,
ChangeFromYearHigh                              decimal,
ChangeFromYearLow                               decimal,
PercentChangeFromYearHigh                       decimal,
PercentChange                                   decimal,
PercentChangeFromFiftydayMovingAverage          decimal,
PercentChangeFromTwoHundreddayMovingAverage     decimal,
PercentChangeFromYearLow                        decimal,
PRIMARY KEY (date, code),
FOREIGN KEY (code) REFERENCES company(code)
);"

createEps="CREATE TABLE eps (
date			                date,
code           			        text,
EPSEstimateCurrentYear          decimal,
EPSEstimateNextQuarter          decimal,
PriceEPSEstimateCurrentYear     decimal,
PriceEPSEstimateNextYear        decimal,
PRIMARY KEY (date, code),
FOREIGN KEY (code) REFERENCES company(code)
);"

createDaily="CREATE TABLE daily (
date		            date,
code           		    text,
volume                  bigint,
DaysHigh                decimal,
DaysLow                 decimal,
BookValue               decimal,
open                    decimal,
PreviousClose           decimal,
PriceBook               decimal,
DividendShare           decimal,
DividendYield           decimal,
EarningsShare           decimal,
MarketCapitalization    bigint,
YearHigh                decimal,
YearLow                 decimal,
PERatio                 decimal,
PriceSales              decimal,
EBITDA                  decimal,
PRIMARY KEY (date, code),
FOREIGN KEY (code) REFERENCES company(code)
);"

declare -a queries

queries[0]="${createIndustry}"
queries[1]="${createCountry}"
queries[2]="${createCompany}"
queries[3]="${createHistoric}"
queries[4]="${createAverages}"
queries[5]="${createChange}"
queries[6]="${createEps}"
queries[7]="${createDaily}"

for query in "${queries[@]}" ; do
	psql -d stockmarket -U ${user} -c "${query}"
done

exit 0

