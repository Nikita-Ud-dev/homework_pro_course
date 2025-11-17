import threading

user_current = threading.local()

def set_current_user(user):
    user_current.value = user

def get_current_user():
    return getattr(user_current, 'value', None)
