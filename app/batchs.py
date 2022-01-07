from . import db
from datetime import datetime, timedelta

def batch_transVideos():
    
    print('batch_transVideos : ', datetime.now())
    db.session.commit()