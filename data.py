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


def get_weighing(telegram_id, for_time):
    if for_time is None:
        weighing = session.query(User).filter(User.telegram_id == telegram_id).first()
    else:
        delta_in_days = datetime.utcnow() - timedelta(days=for_time)
        weighing = session.query(Weight).join(User).filter(User.telegram_id == telegram_id) \
            .filter(Weight.created_at > delta_in_days).all()
    return weighing



