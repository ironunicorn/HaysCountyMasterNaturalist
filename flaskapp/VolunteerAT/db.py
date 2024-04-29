import os

import pymysql
import click
from flask import current_app, g


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def get_db():
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'localhost'
    DATABASE_NAME = os.environ.get('DATABASE_NAME') or 'hcmn'
    DATABASE_USER = os.environ.get('DATABASE_USER') or 'root'
    DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD') or 'armadillo'
    if 'db' not in g:
        g.db = pymysql.connect(
            host=DATABASE_URL,
            database=DATABASE_NAME,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            autocommit=True
        )

    return g.db.cursor()



def init_db():
    try:
        with get_db() as cursor:
            cursor.execute("DROP TABLE IF EXISTS opportunities;")
            cursor.execute("DROP TABLE IF EXISTS master_naturalist;")
            cursor.execute(
                """CREATE TABLE master_naturalist (
                      id INT AUTO_INCREMENT PRIMARY KEY,
                      created DATETIME DEFAULT CURRENT_TIMESTAMP,
                      email VARCHAR (255) UNIQUE NOT NULL,
                      password LONGBLOB NOT NULL,
                      admin TINYINT(1) DEFAULT 0,
                      project_coordinator TINYINT(1) DEFAULT 0
                );"""
            )
            cursor.execute(
                """CREATE TABLE opportunities (
                      id INT AUTO_INCREMENT PRIMARY KEY,
                      created DATETIME DEFAULT CURRENT_TIMESTAMP,
                      owner INT,
                      title VARCHAR (150) NOT NULL,
                      body LONGTEXT NOT NULL,
                      anywhere TINYINT(1) DEFAULT 0,
                      anytime TINYINT(1) DEFAULT 0,
                      location VARCHAR (255),
                      city VARCHAR (50),
                      event_start DATETIME,
                      event_end DATETIME,
                      expiration_date DATETIME,
                      category VARCHAR (50),
                      project_id VARCHAR (50),
                      recurring_weekly TINYINT(1) DEFAULT 0,
                      recurring_monthly INT,
                      link VARCHAR (255),
                      just_show_up TINYINT(1) DEFAULT 0,
                      CONSTRAINT fk_category FOREIGN KEY (owner)
                                             REFERENCES master_naturalist(id)
                );"""
            )
        close_db()
    except Exception as error:
        print(error)



# console command: flask --app VolunteerAT init-db
@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
