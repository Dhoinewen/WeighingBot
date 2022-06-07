from model import User, session


def create_user(telegram_id, telegram_username):
    registered = True
    print(telegram_username, telegram_id)
    if session.query(User).filter(User.telegram_id == telegram_id).first() is None:
        registered = True
        user = User(telegram_id=telegram_id, telegram_username=telegram_username)
        session.add(user)
        session.commit()
        return registered
    else:
        registered = False
        return registered

def create_weighing(telegram_id, weig):
    print('hui')


