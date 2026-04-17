import psycopg2


conn = psycopg2.connect(host="-.-.-.-",database="-",user="-",password="-")
cursor = conn.cursor()

cursor.execute("SELECT * FROM metrics;")

data = cursor.fetchall()
for i in data:
    print(i)


conn.close()
cursor.close()

# insert into database here 