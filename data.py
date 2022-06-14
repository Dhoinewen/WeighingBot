from model import User, session, Weight
from datetime import datetime, timedelta


def create_user(telegram_id, telegram_username):
    registered = True
    if session.query(User).filter(User.telegram_id == telegram_id).first() is None:
        registered = True
        user = User(telegram_id=telegram_id, telegram_username=telegram_username)
        session.add(user)
        session.commit()
        return registered
    else:
        registered = False
        return registered


def create_weighing(telegram_id, weight):
    weighing = Weight(weight=float(weight))
    session.add(weighing)
    session.commit()
    user = session.query(User).filter(User.telegram_id == telegram_id).first()
    user.weights.append(weighing)
    session.commit()


def get_all_weighing(telegram_id):
    return session.query(User).filter(User.telegram_id == telegram_id).first()


def get_seven_days_get_all_weighing(telegram_id):
    seven_days = datetime.utcnow() - timedelta(days=7)
    weighing_last_seven_days = session.query(Weight).filter(Weight.created_at > seven_days.date()).all()


