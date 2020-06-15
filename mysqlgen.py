import mysql.connector
from mysql.connector import Error
from beautifultable import BeautifulTable
import random

enos = [7369, 7499, 7521, 7566, 7654, 7698, 7782, 7788, 7839, 7844, 7876, 7900, 7902, 7934]

enames = [
    'SMITH',
    'ALLEN',
    'WARD',
    'JONES',
    'MARTIN',
    'BLAKE',
    'CLARK',
    'SCOTT',
    'KING',
    'TURNER',
    'ADAMS',
    'JAMES',
    'FORD',
    'MILLER'
]

jobs = [
    'CLERK',
    'SALESMAN',
    'SALESMAN',
    'MANAGER',
    'SALESMAN',
    'MANAGER',
    'MANAGER',
    'ANALYST',
    'PRESIDENT',
    'SALESMAN',
    'CLERK',
    'CLERK',
    'ANALYST',
    'CLERK'
]

hiredates = [
    '1980-12-17',
    '1981-02-20',
    '1981-02-22',
    '1981-04-02',
    '1981-09-28',
    '1981-01-05',
    '1981-06-09',
    '1987-04-19',
    '1981-11-17',
    '1981-09-08',
    '1987-05-23',
    '1981-12-03',
    '1981-12-03',
    '1982-01-03'
]

mgr = [
    7902,
    7698,
    7698,
    7839,
    7698,
    7839,
    7839,
    7566,
    'NULL',
    7698,
    7788,
    7698,
    7566,
    7782
]

sal = [
    800,
    1600,
    1250,
    2975,
    1250,
    2850,
    2450,
    3000,
    5000,
    1500,
    1100,
    950,
    3000,
    1300
]

comm = [
    'NULL',
    300,
    500,
    'NULL',
    1400,
    'NULL',
    'NULL',
    'NULL',
    'NULL',
    0,
    'NULL',
    'NULL',
    'NULL',
    'NULL',
]

deptno = [20, 30, 30, 20, 30, 30, 10, 20, 10, 30, 20, 30, 20, 10]

Ddeptno = [10, 20, 30, 40]
Dname = ['ACCOUNTING', 'RESEARCH', 'SALES', 'OPERATIONS']
Dloc = ['NEW YORK', 'DALLAS', 'CHICAGO', 'BOSTON']

myDb = mysql.connector.connect(
host='localhost',
database=input('Enter database name: '),
user='root',
password=input('Enter password: ')
)

cursor = myDb.cursor()


def execute_query(query, undo = ''):
    cursor.execute(query)
    if query.split()[0] != 'SELECT':
        myDb.commit()
        cursor.execute('SELECT * FROM EMP;')
    records = cursor.fetchall()
    headers = list(cursor.column_names)
    table = output(headers, records)
    if undo:
        cursor.execute(undo)
        myDb.commit()
    return table

def generate_data():
    cursor.execute('DROP TABLE IF EXISTS EMP;')
    cursor.execute('DROP TABLE IF EXISTS EMPLOYEE;')
    myDb.commit()

    cursor.execute('CREATE TABLE EMP (EMPNO INTEGER, ENAME VARCHAR(20), JOB VARCHAR(20), HIREDATE DATE, MGR INTEGER, SAL INTEGER, COMM INTEGER, DEPTNO INTEGER);')
    myDb.commit()

    for i in range(len(enames)):
        line = f"{enos[i]}, '{enames[i]}', '{jobs[i]}', '{hiredates[i]}', {mgr[i]}, {sal[i]}, {comm[i]}, {deptno[i]}"
        query = f'INSERT INTO EMP VALUES({line});'
        cursor.execute(query)
        myDb.commit()

    cursor.execute('DROP TABLE IF EXISTS DEPT;')
    myDb.commit()

    cursor.execute('CREATE TABLE DEPT (DEPTNO INTEGER, DNAME VARCHAR(20), LOC VARCHAR(20), PRIMARY KEY (DEPTNO));')
    myDb.commit()
    
    for j in range(len(Dname)):
        line = f"{Ddeptno[j]}, '{Dname[j]}', '{Dloc[j]}'"
        query = f'INSERT INTO DEPT VALUES({line});'
        cursor.execute(query)
        myDb.commit()
    
    cursor.execute("ALTER TABLE EMP ADD FOREIGN KEY (DEPTNO) REFERENCES DEPT(DEPTNO);")
    myDb.commit()


def output(headers, records):
    table = BeautifulTable()
    table.column_headers = headers
    for row in records:
        row = [x if x is not None else 'NULL' for x in row]
        table.append_row(row)
    return str(table)

def closeDb():
    if (myDb.is_connected()):
        myDb.close()
        cursor.close()
        print("MySQL connection is closed")

generate_data()