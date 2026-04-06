import requests

# Список ID компаний, которые интересуют
company_ids = ['1455', '3529', '3776', '4742', '78638', '15478', '6984', '2432', '9510', '1026']


# Функция для получения данных о компании
def get_company_data(company_id):
    url = f'https://api.hh.ru/employers/{company_id}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Ошибка получения данных о компании {company_id}: {response.status_code}")
        return None


# Функция для получения данных о вакансиях компании
def get_vacancies_data(company_id):
    vacancies_url = f'https://api.hh.ru/vacancies?employer_id={company_id}'
    response = requests.get(vacancies_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Ошибка получения данных о вакансиях компании {company_id}: {response.status_code}")
        return None
