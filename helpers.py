from model import session, Weight
from datetime import datetime


def read_token(file_name):
    with open(file_name, 'r') as file:
        token = file.readline()
    return token


def from_object_user_to_str(data):
    text = ''
    for data in data.weights:
        text += str(data) + ' kg ' + data.created_at.strftime("<u>%Y-%m-%d</u>") + '\n'
    return text


def from_object_weight_to_str(data):
    text = ''
    for weight in data:
        text += str(weight) + ' kg ' + weight.created_at.strftime("<u>%Y-%m-%d</u>") + '\n'
    return text


def check_weight(message_weight):
    try:
        float_message = float(message_weight)
    except ValueError:
        print('Error in message with weight')
        return False
    if float_message > 130 or float_message < 40:
        return False
    return float_message


def weighing_was_today():
    last_weight = session.query(Weight).order_by(Weight.id.desc()).first()
    if datetime.now().date() == last_weight.created_at.date():
        return False
    else:
        return True
