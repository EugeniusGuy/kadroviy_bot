import logging
import typing

import cachetools
import requests

socket = "http://backend:80"

logger = logging.getLogger(__name__)
# получение должностей
def fetch_available_posts(filters="") -> typing.Dict:
    logger.info(f"Поиск должностей в: {filters}")
    response = requests.get(
        socket+"/api/judgment/vacancy/types"
        +filters,
        headers={
            # "Authorization": AIRTABLE_TOKEN,
        },
    )
    logger.info(response.json())
    return response.json()

def fetch_persons_info(filters=""):
    logger.info(f"Поиск районов для должности: {filters}")
    response = requests.get(
        socket+"/api/judgment/district?vacancy="
        +filters,
        headers={
            # "Authorization": AIRTABLE_TOKEN,
        },
    )
    logger.info(response.json())
    return response.json()

def fetch_candidate_status(tgid=""):
    logging.info(f"Статус заявки по id {tgid}")
    response = requests.get(
        socket+"/api/candidate/" + str(tgid) + "/check-status",
        headers={
            # "Authorization": AIRTABLE_TOKEN,
        },
    )
    logger.info(response.json())
    return response.json()

def post_candidate(name: str, surname: str, last_name:str, email: str, tgid: str, id_judgement_place):
    logging.info(f"POST candidate {name}, {surname}, {last_name}, {email}, {tgid}, {id_judgement_place}")
    data = {
        "name": name,
        "surname": surname,
        "last_name": last_name,
        "email": email,
        "telegram_id": tgid,
        "id_judgement_place": id_judgement_place
    }
    response = requests.post(
        socket+"/api/candidate/",
        headers={
            # "Authorization": AIRTABLE_TOKEN,
        },
        json=data
    )
    logger.info(response.json())
    return response.json()

def fetch_judgement_place_byid(filters):
    logger.info(f'Поиск информации по участку {filters}')
    response = requests.get(
        socket+"/api/judgment/"
        +filters,
        headers={
            # "Authorization": AIRTABLE_TOKEN,
        },
    )
    logger.info(response.json())
    return response.json()


def get_unique_data_by_field(field: "str", table_func) -> typing.List["str"]:

    records = table_func()
    unique_set_list = set()

    for record in records:
        unique_set_list.add(record["fields"][field])

    return list(unique_set_list)

def fetch_judgment_places(district: "str", post: "int",):
    logging.info(f"Поиск участка по району {district} должности: {post}")
    response = requests.get(
        socket+"/api/judgment/",
        headers={
            # "Authorization": AIRTABLE_TOKEN,
        },
    )
    logging.info(f"Участки без фильтра {response.json()}")
    #  a_list = json.loads(response.json())
    filtered_response = [
         dictionary for dictionary in response.json()
         if dictionary['district'] == district and post in dictionary['vacancies']
     ]
    logger.info(f'Отфильтрованный результат по поиску участков: {filtered_response}')
    return filtered_response

def resend_document_status(tg_id):
    logger.info(f"resend_document_status: {tg_id}")
    response = requests.put(
        socket+f"/api/candidate/{tg_id}/recheck-status"
    )
    logger.info(response.json())
    return response.json()
