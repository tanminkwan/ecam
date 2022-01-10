from flask import g
import enum
import uuid
import socket

def get_user():
    return g.user.username

def get_hostname():
    return socket.gethostname()

def get_uuid():
    return str(uuid.uuid4())[-12:]

class YnEnum(enum.Enum):
    YES = 'YES'
    NO  = 'NO'