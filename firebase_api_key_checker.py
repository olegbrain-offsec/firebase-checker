import os, argparse
import sys
from multiprocessing import freeze_support
from typing import Dict

sys.path.append(os.getcwd())

from utils.string_utils import remove_new_lines, restrict_string_length
from utils.web import RequestConfig, post_request, send_requests, to_curl

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Read args
parser = argparse.ArgumentParser(description='Firebase app checker')
parser.add_argument('-email', type=str, help='Email to register in firebase proj',required=False, default='justtest@gmail.com')
parser.add_argument('-passwd', type=str, help='Password for testing registration',required=False, default='S3cur3P4ssW0rd!')
parser.add_argument('-apikey', type=str, help='Firebase leaked API key',required=True)
parser.add_argument('-project', type=str, help='Firebase project id (project_id.firebaseio.com, project_id.firebaseio.com)',required=True)


args = parser.parse_args()

email = args.email
password = args.passwd
print(f"Using credentials: {email}, password {password}")
api_key = args.apikey
project_id = args.project
print(f"Checking: {project_id} with API key: {api_key}")
firebase_host = f'{project_id}.firebaseio.com'  # like https://project_id.firebaseio.com
storage_appspot_host = f'{project_id}.appspot.com'  # like project_id.appspot.com

proxy = ''
proxies = {'https': proxy} if proxy else None
try_to_signup = True



def sign_up(email: str, password: str, api_key: str, proxies: Dict) -> str:
    response = post_request(
        f'https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={api_key}',
        json={
            'email': email,
            'password': password,
            "returnSecureToken": True
        },
        proxies=proxies,
    )
    if response.status_code != 200 or 'idToken' not in response.text:
        raise ValueError(f'registry is not available: {response.status_code}, {response.text}')

    return response.text


def login(email: str, password: str, api_key: str, proxy: str):
    return send_requests([
        RequestConfig(
            f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}',
            body={
                'email': email,
                'password': password,
                "returnSecureToken": True
            },
            json=True,
            method='POST',
        )
    ], proxy=proxy)[0]


def check_firestore(auth_token: str, project_id: str, proxy: str):
    return send_requests([
        RequestConfig(
            f'https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents/definitelynotexistedcollection',
            headers={
                'Authorization': f'Bearer {auth_token}',
            },
        )
    ], proxy=proxy)


def check_firebase(auth_token: str, firebase_host: str, proxy: str):
    firebase_host = 'https://' + firebase_host if not firebase_host.startswith('https://') else firebase_host
    return send_requests([
        RequestConfig(
            f'{firebase_host}/.json?auth={auth_token}',
        ),
        RequestConfig(
            f'{firebase_host}/definitelynotexistedcollection.json?auth={auth_token}',
        ),
        RequestConfig(
            f'{firebase_host}/.settings/rules.json?access_token={auth_token}',
        ),
    ], proxy=proxy)


def check_appspot(auth_token: str, storage_appspot_host: str, proxy: str):
    return send_requests([
        RequestConfig(
            f'https://firebasestorage.googleapis.com/v0/b/{storage_appspot_host}/o/',
            headers={
                'Authorization': f'Bearer {auth_token}',
            },
        )
    ], proxy=proxy)


if __name__ == '__main__':
    freeze_support()

    if try_to_signup:
        sign_up_response = sign_up(email, password, api_key, proxies)
        print(f'SignUp response: {sign_up_response}')

    login_config, login_response = login(email, password, api_key, proxy)
    print(f'Login response: {login_response.status} {login_response.text}')
    if login_response.status != 200 or 'idToken' not in login_response.text:
        raise ValueError(f'Login by email and password is not available: {login_response.status}, {login_response.text}')
    print(to_curl(login_config))

    auth_token = login_response.json().get('idToken')
    print(f'Your auth token: {auth_token}')

    print('----------------------------------------')
    if project_id:
        firestore_responses = check_firestore(auth_token, project_id, proxy)
        for config, firestore_response in firestore_responses:
            print(f'\nFirestore response: {firestore_response.status} {remove_new_lines(firestore_response.text)}')
            if firestore_response.status == 200 and remove_new_lines(firestore_response.text) == '{}':
                print('Firestore IS VULNERABLE because it returns empty object, now just bruteforce collection names.')
                print(to_curl(config))
            else:
                print('Firestore seems not vulnerable')

    print('----------------------------------------')
    if firebase_host:
        firebase_responses = check_firebase(auth_token, firebase_host, proxy)
        for config, firebase_response in firebase_responses:
            print(
                f'\n\nFirebase response: \n {firebase_response.url} \n status code: {firebase_response.status}'
                f' \n response: {restrict_string_length(firebase_response.text, 100)}')
            if firebase_response.status == 200:
                print('it seems VULNERABLE because of 200 status, otherwise it would be 401')
                print(to_curl(config))
            else:
                print(f'it seems not vulnerable because of status code: {firebase_response.status}')

    print('----------------------------------------')
    if storage_appspot_host:
        appspot_responses = check_appspot(auth_token, storage_appspot_host, proxy)
        for config, appspot_response in appspot_responses:
            print(f'\nAppspot response: {appspot_response.status} {remove_new_lines(appspot_response.text)}')
            if appspot_response.status == 200 and len(appspot_response.text) > 10:
                print('Appspot IS VULNERABLE, just check response.')
                print(to_curl(config))
            else:
                print('Appspot seems not vulnerable')
