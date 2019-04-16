import clearbit
import requests
from django.conf import settings

clearbit.key = settings.CLEARBIT_API_KEY


def validate_email(email):
    """
    Send GET request to Email Hunter API and get response.
    :param email: str, E-Mail to verify.
    :return: True if email is valid and False if not.
    """
    url = (f'{settings.EMAIL_HUNTER_BASE_URL}?email={email}'
           f'&api_key={settings.EMAIL_HUNTER_API_KEY}')

    response = requests.get(url)
    response = response.json()

    mx_records = response['data']['mx_records']
    smtp_server = response['data']['smtp_server']
    smpt_check = response['data']['smtp_check']

    if all([mx_records, smtp_server, smpt_check]):
        return True

    return False


def get_additional_info(email):
    """
    Look up person and company data based on an email or domain.
    :param email: str, Email
    :return: dictionary, Response from Clearbit API server
    """
    response = clearbit.Enrichment.find(email=email, stream=True)
    return response
