

def from_oject_to_str(data):
    text = ''
    for data in data.weights:
        print(data, 'kg', data.created_at.strftime("%Y-%m-%d %H:%M"))
        text += str(data) + ' kg ' + data.created_at.strftime("%Y-%m-%d %H:%M") + '\n'
    return text

