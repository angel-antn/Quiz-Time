import requests
import html
from question_model import Question


def get_questions():
    params = {
        'amount': '10',
        'type': 'boolean',
    }

    data = requests.get('https://opentdb.com/api.php', params=params)
    data.raise_for_status()
    data_questions = data.json()['results']

    questions = []

    for i in data_questions:
        i['question'] = html.unescape(i['question'])
        questions.append(Question(i['question'], i['correct_answer']))

    return questions


def have_internet():
    try:
        requests.get("https://www.google.com", timeout=5)
    except (requests.ConnectionError, requests.Timeout):
        return False
    else:
        return True
