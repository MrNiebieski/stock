# Kavin Autar
# 2013/11/14
# Version 1.3
# Checks stocks db module


import logger as log
import psycopg2

dbname = "stockmarket"
user = "kav"

def dbConn():
    global dbname
    global user
    conn = psycopg2.connect("dbname=%s user=%s" % (dbname, user))
    isql = conn.cursor()
    log.info("created DB connection", "with user", user, "db", dbname, str(type(conn)))
    return conn, isql


def insertSingle(query, values):
    conn, isql = dbConn()
    log.debug("trying to execute query %s with vars %s" % (query, values))
    try:
        isql.execute(query, values)
        log.info("executing %s with vars %s" % (query, " ".join(values)))
    except psycopg2.IntegrityError as e:
        log.error("\"%s\"" % " ".join(values), "already exists",  str(e))
        conn.rollback()
    except psycopg2.ProgrammingError as e:
        log.error("sql error when running", query, "with values", " ".join(values))
        conn.rollback()
    except Exception as e:
        eType = e.__class__.__name__
        log.error("unable to run query %s with vars %s due to error %s" % (query, values, str(e)), "UNHANDLED EXCEPTION:", eType)
        conn.rollback()
    else:
        log.info("query success:", query, "with values", " ".join(values))
        conn.commit()
    finally:
        log.info("closing db connection")
        conn.close()

def main():
    print "main function"
    temp = []
    temp.append("software")
    insertSingle("INSERT INTO INDUSTRY (name) values (%s);", temp)


if __name__ == "__main__":
    main()
