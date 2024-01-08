import mysql.connector
from mysql.connector import Error
import os
db_password = os.getenv('db_password')
def create_connection(host_name, user_name, user_password, db_name=None):
    connection = None
    try:
        if db_name:
            connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                passwd=user_password,
                database=db_name
            )
        else:
            connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                passwd=user_password
            )
        print("MySQL Database connection successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def create_database(connection, db_name):
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Database {db_name} created successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
def create_table(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Table created successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
# MySQL 서버에 연결
connection = create_connection("127.0.0.1", "root", db_password)

# 데이터베이스 생성
create_database(connection, "lck_betting_db")

# 데이터베이스를 선택하기 위해 연결을 다시 설정
connection.close()  # 이전 연결 닫기
connection = create_connection("127.0.0.1", "root", db_password, "lck_betting_db")

# Users 테이블 생성
create_users_table = """
CREATE TABLE IF NOT EXISTS Users (
    DiscordID BIGINT PRIMARY KEY,
    Points INT
);
"""
create_table(connection, create_users_table)

# Bets 테이블 생성
create_bets_table = """
CREATE TABLE IF NOT EXISTS Bets (
    BetID INT AUTO_INCREMENT PRIMARY KEY,
    DiscordID BIGINT,
    Week INT,
    MatchID INT,
    TeamChoice INT,
    BetAmount INT,
    BetTime DATETIME,
    FOREIGN KEY (DiscordID) REFERENCES Users(DiscordID)
);
"""
create_table(connection, create_bets_table)

# Matches 테이블 생성
create_matches_table = """
CREATE TABLE IF NOT EXISTS Matches (
    MatchID INT PRIMARY KEY,
    Team1 VARCHAR(255),
    Team2 VARCHAR(255),
    MatchDateTime DATETIME,
    Result INT
);
"""
create_table(connection, create_matches_table)
