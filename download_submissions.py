from bs4 import BeautifulSoup
import unicodedata
import json
import re
import os
import requests

BASE_URL = 'https://sapientia.progcont.eu'
OVERVIEW_URL = f'{BASE_URL}/ecn/overview'
LOGIN_URL = f'{BASE_URL}/ecn/login'
COOKIE_NAME = 'JSESSIONID'
EXTENSIONS = {
    'C++': 'cpp',
    'Java': 'java',
    'ANSI C': 'c'
}

def slugify(value):
    value = unicodedata.normalize('NFKC', value)
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

def find_number(str):
    return re.search(r'\d+', str).group()

def get_problem_url(problem_id):
    return f'{BASE_URL}/ecn/problem?pid={problem_id}'

def get_download_url(download_id):
    return f'{BASE_URL}/ecn/download?si={download_id}'

def login(username, password):
    print(f'Logging in with user: {username}...')

    formdata = {'action': 'login', 'username': username, 'password': password}
    req = requests.post(LOGIN_URL, data=formdata, allow_redirects=False)
    cookies = req.cookies

    if COOKIE_NAME not in cookies:
        raise Exception(f'Failed to login with user {username}')
    
    return cookies

def get_problems(cookies):
    print('Finding problems...')

    req = requests.get(OVERVIEW_URL, cookies=cookies)
    soup = BeautifulSoup(req.text, 'html.parser')

    container = soup.find_all('div', {'class': 'main-container'})[1]
    rows = container.find_all('div', {'class': 'row'})
    problems = []

    for row in rows:
        divs = row.find_all('div')
        link = divs[6].find_all('a')[0]
        problem_id = find_number(link['href'])
        problem_name = link.text

        problems.append({
            'id': problem_id,
            'name': problem_name
        })
    
    return problems

def get_downloads(cookies, problem_id):
    print(f'Finding downloads for problem {problem_id}...')
    req = requests.get(get_problem_url(problem_id), cookies=cookies)
    req.raise_for_status()
    soup = BeautifulSoup(req.text, 'html.parser')

    container = soup.find_all('div', {'class': 'main-container'})[1]
    rows = container.find_all('div', {'class': 'row'})
    downloads = []

    for row in rows:
        divs = row.find_all('div')
        language = divs[2].text.strip()
        link = divs[5].find_all('a')[0]
        download_id = find_number(link['href'])
        passing = divs[3].text.strip().lower() == 'pass'

        if language not in EXTENSIONS:
            raise Exception(f'Unknown language: {language}')

        downloads.append({
            'id': download_id,
            'language': language,
            'passing': passing
        })
    
    downloads.reverse()
    return downloads

def download_solution(cookies, problem_name, team_name, entry, number):
    entry_id = entry['id']
    passed = 'pass' if entry['passing'] else 'fail'
    folder_name = slugify(problem_name)

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    team_name = slugify(team_name)
    extension = EXTENSIONS[entry['language']]
    filename = os.path.join(folder_name, f'{team_name}_{number}_{passed}.{extension}')

    if os.path.exists(filename):
        return

    print(f'Downloading problem solution: {entry_id}...')

    req = requests.get(get_download_url(entry_id), cookies=cookies)
    req.raise_for_status()

    with open(filename, 'wb') as f:
        f.write(req.content)

def download_all_by_user(user):
    team_name = user['team']
    username = user['username']
    password = user['password']

    cookies = login(username, password)
    problems = get_problems(cookies)

    for problem in problems:
        download_entries = get_downloads(cookies, problem['id'])

        for i, download_entry in enumerate(download_entries):
            download_solution(cookies, problem['name'], team_name, download_entry, i + 1)

with open('users.json', 'r', encoding='utf-8') as f:
    users = json.load(f)

for user in users:
    download_all_by_user(user)
