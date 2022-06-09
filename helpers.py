def read_token(file_name):
    with open(file_name, 'r') as file:
        token = file.readline()
    return token


def from_oject_to_str(data):
    text = ''
    for data in data.weights:
        text += str(data) + ' kg ' + data.created_at.strftime("%Y-%m-%d %H:%M") + '\n'
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