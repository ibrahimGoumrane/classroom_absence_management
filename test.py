import MySQLdb
try:
    conn = MySQLdb.connect(host='127.0.0.1', user='admin', passwd='root', db='classroom_db', port=3307)
    print("Connection successful!")
except MySQLdb.OperationalError as e:
    print(f"Error: {e}")