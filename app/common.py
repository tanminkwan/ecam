from flask import g
import enum
import uuid
import socket
from .queries import selectRow

def get_user():
    return g.user.username

def get_hostname():
    return socket.gethostname()

def get_uuid():
    return str(uuid.uuid4())[-12:]

def get_thumbnailpath(stored_filename):
    
    filter_dict = dict(
        ref_stored_filename = stored_filename
    )    
    rec, _ = selectRow('content_master', filter_dict)
    
    return rec.manifest_path if rec else ''
    
class YnEnum(enum.Enum):
    YES = 'YES'
    NO  = 'NO'