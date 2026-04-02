from src.files import create_database, create_tables, insert_company_data, insert_vacancy_data
from src.api import get_company_data, get_vacancies_data
from src.vacansies import DBManager


def main():
    # Создание базы данных и таблиц
    try:
        create_database()
        print("База данных успешно создана.")
    except Exception as e:
        print(f"Ошибка создания базы данных: {e}")

    try:
        create_tables()
        print("Таблицы успешно созданы.")
    except Exception as e:
        print(f"Ошибка создания таблиц: {e}")

    # Заполнение таблиц данными из API hh.ru
    company_ids = ['1455', '3529', '3776', '4742', '78638', '15478', '6984', '2432', '9510', '1026']
    for company_id in company_ids:
        company_data = get_company_data(company_id)
        if company_data:
            insert_company_data(company_data)

        vacancies_data = get_vacancies_data(company_id)
        if vacancies_data:
            for vacancy in vacancies_data['items']:
                insert_vacancy_data(vacancy)

    print("Данные успешно загружены в базу данных.")

    # Интерфейс взаимодействия с пользователем
    db_manager = DBManager()

    try:
        while True:
            print("\nДобро пожаловать в систему управления вакансиями!")
            print("Пожалуйста, выберите действие:")
            print("1 - Показать все компании и количество их вакансий")
            print("2 - Показать все вакансии")
            print("3 - Показать среднюю зарплату по вакансиям")
            print("4 - Показать вакансии с зарплатой выше средней")
            print("5 - Поиск вакансий по ключевому слову")
            print("0 - Выход")

            choice = input("Введите номер действия: ")

            if choice == '1':
                companies = db_manager.get_companies_and_vacancies_count()
                print("\nСписок компаний и количество вакансий:")
                for company, count in companies:
                    print(f"Компания: {company}, Количество вакансий: {count}")

            elif choice == '2':
                vacancies = db_manager.get_all_vacancies()
                print("\nСписок всех вакансий:")
                for company_name, vacancy_name, salary_from, salary_to, link in vacancies:
                    salary_info = f"{salary_from} - {salary_to}" if salary_from and salary_to else "Не указана"
                    print(
                        f"Компания: {company_name}, Вакансия: {vacancy_name}, Зарплата: {salary_info}, Ссылка: {link}")

            elif choice == '3':
                avg_salary = db_manager.get_avg_salary()
                print(f"\nСредняя зарплата по вакансиям: {avg_salary:.2f}")

            elif choice == '4':
                higher_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
                print("\nВакансии с зарплатой выше средней:")
                for vacancy_name, company_name, salary_from, salary_to in higher_salary_vacancies:
                    salary_info = f"{salary_from} - {salary_to}" if salary_from and salary_to else "Не указана"
                    print(f"Компания: {company_name}, Вакансия: {vacancy_name}, Зарплата: {salary_info}")

            elif choice == '5':
                keyword = input("Введите ключевое слово для поиска: ")
                keyword_vacancies = db_manager.get_vacancies_with_keyword(keyword)
                print(f"\nВакансии, содержащие '{keyword}' в названии:")
                for vacancy_name, company_name, salary_from, salary_to in keyword_vacancies:
                    salary_info = f"{salary_from} - {salary_to}" if salary_from and salary_to else "Не указана"
                    print(f"Компания: {company_name}, Вакансия: {vacancy_name}, Зарплата: {salary_info}")

            elif choice == '0':
                print("Выход из программы.")
                break

            else:
                print("Неверный ввод. Пожалуйста, выберите действие из списка.")

    finally:
        db_manager.close()


if __name__ == "__main__":
    main()
