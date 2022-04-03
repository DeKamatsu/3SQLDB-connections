import time
import sqlite3
from sqlite3 import Error


connection1 = None
try:
    connection1 = sqlite3.connect('belhard.db')  # коннектор для соединения программы с БД
except Error as er:
    print(er)
cursor_SQLlite = connection1.cursor()


def insert(first_name, second_name):
    cursor_SQLlite.execute(f"INSERT INTO user (first_name, second_name) VALUES('{first_name}', '{second_name}');")
    connection1.commit()


try:  # creation & manual input in new table 'user' for first time
    cursor_SQLlite.execute("CREATE TABLE user (id SERIAL, first_name text, second_name text);")
    for _ in range(7):
        f_name = input("Введите имя: ")
        l_name = input("Введите фамилию: ")
        insert(f_name, l_name)
except Error as er:
    print(er)

try:
    cursor_SQLlite.execute("DROP TABLE family")  # delete existing table 'family'
    cursor_SQLlite.execute("DROP TABLE family")  # 2-nd deleting existing table 'family' to work with exception
except Error as er:
    print(er)

try:  # creation of second new table 'family' and fields copying from existing table 'user'
    cursor_SQLlite.execute("CREATE TABLE family (id SERIAL, first_name text, second_name text);")
    cursor_SQLlite.execute("SELECT first_name, second_name FROM user")
    temp_BD = cursor_SQLlite.fetchall()  # getting all data in list
    for t in temp_BD:
        cursor_SQLlite.execute(f"INSERT INTO family (first_name, second_name) VALUES('{t[0]}', '{t[1]}')")
except Error as er:
    print(er)


cursor_SQLlite.execute("UPDATE family SET first_name='Helen' WHERE first_name='Elena'")

cursor_SQLlite.execute("SELECT first_name, second_name FROM user")
usr = cursor_SQLlite.fetchall()

for t in usr:  # print all users
    print(f"usr from mySQL: {t}")

# cur.execute("DROP family")

tmp = time.time()
cursor_SQLlite.execute("SELECT first_name, second_name FROM family")
fam = cursor_SQLlite.fetchall()
t_SQLlite = time.time() - tmp

for t in fam:  # print all family
    print(f"fam: {t}")

connection1.close()


t = time.time()


import mysql.connector as mysql  # import from MySQL lib
# from mysql.connector import Error
from decouple import config


connection2 = mysql.connect(host='localhost',  # connector MySQL
                            database='belhard',
                            user=config('userID_mySQL', default=''),
                            password=config('password_mySQL', default=''))
cursor_mySQL = connection2.cursor()

tmp = time.time()
cursor_mySQL.execute("SELECT firstname, lastname FROM family")
fam = cursor_mySQL.fetchall()
t_mySQL = time.time() - tmp

for t in fam:  # print all family
    print(f"fam from MySQL: {t}")

connection2.close()


import psycopg2  # import from PosgreSQL

connection3 = psycopg2.connect(host='localhost',  # connector PostgreSQL
                               database='belhard',
                               user=config('userID_PostgreSQL', default=''),
                               password=config('password_PostgreSQL', default=''))
cursor_postgreSQL = connection3.cursor()

tmp = time.time()
cursor_postgreSQL.execute("SELECT firstname, lastname FROM family")
t_psgSQL = time.time() - tmp

for t in fam:  # print all family
    print(f"fam from PostgreSQL: {t}")

connection3.close()

print('Time of selecting from SQLite:', t_SQLlite)
print('Time of selecting from mySQL:', t_mySQL)
print('Time of selecting from PostgreSQL:', t_psgSQL)

