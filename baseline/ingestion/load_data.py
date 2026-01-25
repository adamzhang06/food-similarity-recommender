import psycopg2

conn = psycopg2.connect(
    dbname="fooddb",
    user="fooduser",
    password="foodpass",
    host="localhost",
    port=5432
)
