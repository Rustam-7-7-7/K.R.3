import psycopg2
from config import config


class DBManager:
    def __init__(self):
        # Подключение к базе данных
        params = config()
        self.conn = psycopg2.connect(
            dbname=params['database'],
            user=params['user'],
            password=params['password'],
            host=params['host']
        )
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        # Получение списка всех компаний и количества вакансий у каждой
        query = '''
            SELECT c.name, COUNT(v.id) as vacancy_count
            FROM companies c
            LEFT JOIN vacancies v ON c.id = v.employer_id
            GROUP BY c.name
        '''
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_all_vacancies(self):
        # Получение списка всех вакансий с подробной информацией
        query = '''
            SELECT c.name as company_name, v.name as vacancy_name, v.salary_from, v.salary_to, 'https://hh.ru/vacancy/' || v.id as link
            FROM vacancies v
            JOIN companies c ON v.employer_id = c.id
        '''
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_avg_salary(self):
        # Получение средней зарплаты по вакансиям
        query = '''
            SELECT AVG((salary_from + salary_to) / 2.0) as avg_salary
            FROM vacancies
            WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL
        '''
        self.cur.execute(query)
        return self.cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        # Получение списка всех вакансий с зарплатой выше средней
        avg_salary = self.get_avg_salary()
        query = '''
            SELECT v.name, c.name as company_name, v.salary_from, v.salary_to
            FROM vacancies v
            JOIN companies c ON v.employer_id = c.id
            WHERE (v.salary_from + v.salary_to) / 2.0 > %s
        '''
        self.cur.execute(query, (avg_salary,))
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        # Получение списка всех вакансий, содержащих ключевое слово в названии
        query = '''
            SELECT v.name, c.name as company_name, v.salary_from, v.salary_to
            FROM vacancies v
            JOIN companies c ON v.employer_id = c.id
            WHERE v.name ILIKE %s
        '''
        self.cur.execute(query, (f'%{keyword}%',))
        return self.cur.fetchall()

    def close(self):
        # Закрытие соединения с базой данных
        self.cur.close()
        self.conn.close()
