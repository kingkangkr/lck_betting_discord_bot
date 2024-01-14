import mysql.connector
from mysql.connector import Error
import os

db_password = os.getenv('db_password')

# 데이터베이스 연결 설정
connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    passwd=db_password,
    database="lck_betting_db"
)

# Users 테이블에 Name 열 추가
add_name_column = """
ALTER TABLE Users
ADD COLUMN Name VARCHAR(100);
"""

# 쿼리 실행 함수
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as e:
        print(f"The error '{e}' occurred")

# 쿼리 실행
execute_query(connection, add_name_column)
