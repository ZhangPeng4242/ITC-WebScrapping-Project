from src_files.config import config
import sqlparse
import sqlalchemy
from pathlib2 import Path
import pandas as pd


def create_db():
    with open("init_db_myanimelist.sql", "r") as sql_file:
        sql_script = sql_file.read()

    sql_list = sqlparse.split(sql_script)
    with config.connection:
        with config.connection.cursor() as cursor:
            cursor.execute("DROP DATABASE IF EXISTS db_myanimelist")
            for sql in sql_list:
                cursor.execute(sql)

    config.logger.info("Database successfully created!")


def insert_init_data():
    engine = sqlalchemy.create_engine('mysql+pymysql://root:zp2543765@localhost/db_myanimelist?charset=utf8')
    file_list = ['anime.csv', 'people.csv', 'character.csv', 'genre.csv', 'studio.csv', 'voice_actor.csv',
                 'anime_genre.csv', 'studio_anime.csv', 'anime_character.csv', 'anime_watch_stats.csv',
                 'anime_score_stats.csv', 'anime_general_stats.csv', 'staff.csv']
    for file_name in file_list:
        df = pd.read_csv(Path(config.datas_dir) / file_name)
        df.to_sql(file_name[:-4], engine, if_exists="append", index=False)
        config.logger.info(f"Successfully initiated table: {file_name[:-4]}")


def init_db():
    create_db()
    insert_init_data()
    config.logger.info(f"Successfully initiated database: db_myanimelist!")


init_db()