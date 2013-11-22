# Kavin Autar
# 2013/10/28
# Last modified 2013/11/17
# Version 1.4
# Checks stocks db module

# Imports
import logger as log
import psycopg2
import psycopg2.extras
import sys


# Global vars
dbname = "stockmarket_testing"
user = "kav"

# Functions
def dbConn():
    global dbname
    global user

    # try and make a db connection. on error log message
    # returns a psycopg2 connection and cursor
    # should probably have a break point and do something here on error
    try:
        conn = psycopg2.connect("dbname=%s user=%s" % (dbname, user))
        isql = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        log.info("created DB connection", "with user", user, "db", dbname, str(type(conn)))
    except Exception as e:
        eType = e.__class__.__name__
        log.error("unable to conect to database: %s as user: %s due to error" % (dbname, user, str(e)), "UNHANDLED EXCEPTION:", eType)
    else:
        return conn, isql
    

def insertSingle(query, values):
    conn, isql = dbConn()
    sqlString = isql.mogrify(query, values)
    returnVal = False

    # try and execute the query from input
    try:
        log.info("executing query: %s" % sqlString)
        isql.execute(query, values)
    except psycopg2.IntegrityError as e:
        log.error("\"%s\"" % " ".join(values), "already exists",  str(e))
        log.info("rolling back transaction for query %s" % sqlString)
        conn.rollback()
    except psycopg2.ProgrammingError as e:
        log.error("sql error when executing: %s" % sqlString)
        log.info("rolling back transaction for query %s" % sqlString)
        conn.rollback()
    except Exception as e:
        eType = e.__class__.__name__
        log.error("unable to run query %s error %s" % (sqlString, str(e)), "UNHANDLED EXCEPTION:", eType)
        log.info("rolling back transaction for query %s" % sqlString)
        conn.rollback()
    else:
        log.info("query success: %s" % sqlString)
        returnVal = True
        conn.commit()
    finally:
        log.info("closing db connection")
        conn.close()
        return returnVal

def selectQuery(query, values):
    conn, isql = dbConn()
    sqlString = isql.mogrify(query, values)

    try:
        log.info("executing query: %s" % sqlString)
        isql.execute(query, values)
        returnVal = isql.fetchall()
    except Exception as e:
        eType = e.__class__.__name__
        log.error("unable to run query %s error %s" % (sqlString, str(e)), "UNHANDLED EXCEPTION:", eType)
    finally:    
        conn.close()

    return returnVal

def selectQueryNoWhere(query):
    conn, isql = dbConn()
    try:
        log.info("executing query: %s" % query)
        isql.execute(query)
        returnVal = isql.fetchall()
    except Exception as e:
        eType = e.__class__.__name__
        log.error("unable to run query %s error %s" % (sqlString, str(e)), "UNHANDLED EXCEPTION:", eType)
    finally:
        conn.close()

    return returnVal

# Main

def main():
    print "main function"
    temp = []
    temp.append(sys.argv[1])
    insertSingle("INSERT INTO INDUSTRY (name) values (%s);", temp)


if __name__ == "__main__":
    main()
