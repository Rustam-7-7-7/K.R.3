import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import config
from src.api import get_company_data, get_vacancies_data


def create_database():
    params = config()
    conn = psycopg2.connect(
        dbname='postgres',
        user=params['user'],
        password=params['password'],
        host=params['host']
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE {params['database']}")
    cur.close()
    conn.close()


def create_tables():
    params = config()
    conn = psycopg2.connect(
        dbname=params['database'],
        user=params['user'],
        password=params['password'],
        host=params['host']
    )
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY,
            name TEXT,
            description TEXT,
            area TEXT
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS vacancies (
            id INTEGER PRIMARY KEY,
            name TEXT,
            employer_id INTEGER REFERENCES companies(id),
            salary_from INTEGER,
            salary_to INTEGER,
            area TEXT
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()


def insert_company_data(company_data):
    params = config()
    conn = psycopg2.connect(
        dbname=params['database'],
        user=params['user'],
        password=params['password'],
        host=params['host']
    )
    cur = conn.cursor()

    cur.execute('''
        INSERT INTO companies (id, name, description, area)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING
    ''', (company_data['id'], company_data['name'], company_data.get('description', ''), company_data['area']['name']))

    conn.commit()
    cur.close()
    conn.close()


def insert_vacancy_data(vacancy_data):
    params = config()
    conn = psycopg2.connect(
        dbname=params['database'],
        user=params['user'],
        password=params['password'],
        host=params['host']
    )
    cur = conn.cursor()

    salary_from = vacancy_data['salary']['from'] if vacancy_data['salary'] else None
    salary_to = vacancy_data['salary']['to'] if vacancy_data['salary'] else None

    cur.execute('''
        INSERT INTO vacancies (id, name, employer_id, salary_from, salary_to, area)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING
    ''', (vacancy_data['id'], vacancy_data['name'], vacancy_data['employer']['id'], salary_from, salary_to,
          vacancy_data['area']['name']))

    conn.commit()
    cur.close()
    conn.close()
