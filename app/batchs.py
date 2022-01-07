from . import db
from .queries import selectRows

from datetime import datetime, timedelta

def batch_transVideos():
    
    print('batch_transVideos : ', datetime.now())
    filter_dict = dict(name='테스트')
    recs = selectRows('test_table',filter_dict)
    
    for rec in recs:
        print('row : ', rec)
    
    db.session.commit()