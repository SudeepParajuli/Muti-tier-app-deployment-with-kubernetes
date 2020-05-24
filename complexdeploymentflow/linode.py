from flask import Flask
import logging
import psycopg2
import redis
import sys
import os

app = Flask(__name__)
host = os.environ.get("REDIS_HOST")
port = os.environ.get("REDIS_PORT")
dbname = os.environ.get("POSTGRES_DB")
user = os.environ.get("DB_USER")
password = os.environ.get("POSTGRES_PASSWORD")

redis_host_connection = "host=%s port=%s"%(host,port)
cache = redis.StrictRedis(redis_host_connection)

# Configure Logging
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)

def PgFetch(query, method):
    conn_str = "dbname=%s host=%s user = %s port=%s"%(dbname,host,user,port)

    # Connect to an existing database
    #conn = psycopg2.connect("host='postgres' dbname='linode' user='postgres' password='linode123'")
    conn = psycopg2.connect(conn_str)

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Query the database and obtain data as Python objects
    dbquery = cur.execute(query)

    if method == 'GET':
        result = cur.fetchone()
    else:
        result = ""

    # Make the changes to the database persistent
    conn.commit()

    # Close communication with the database
    cur.close()
    conn.close()
    return result

@app.route('/')
def hello_world():
    if cache.exists('visitor_count'):
        cache.incr('visitor_count')
        count = (cache.get('visitor_count')).decode('utf-8')
        update = PgFetch("UPDATE visitors set visitor_count = " + count + " where site_id = 1;", "POST")
    else:
        cache_refresh = PgFetch("SELECT visitor_count FROM visitors where site_id = 1;", "GET")
        count = int(cache_refresh[0])
        cache.set('visitor_count', count)
        cache.incr('visitor_count')
        count = (cache.get('visitor_count')).decode('utf-8')
    return 'Hello Linode!  This page has been viewed %s time(s).' % count

@app.route('/resetcounter')
def resetcounter():
    cache.delete('visitor_count')
    PgFetch("UPDATE visitors set visitor_count = 0 where site_id = 1;", "POST")
    app.logger.debug("reset visitor count")
    return "Successfully deleted redis and postgres counters"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port= 8000,  debug=True)
