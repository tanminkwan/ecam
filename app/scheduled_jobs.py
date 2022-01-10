from . import db, scheduler
from .batchs import updateContentsInfo, batch_transVideos
from datetime import datetime, timedelta

@scheduler.task('cron', id='job_transVideos', name='Auto Transcoding Videos', minute='*/30')
def job_transVideos():
    batch_transVideos()
    
def job_create_job(target):
    
    dynamic_dict = dict(trigger = 'date'\
        , run_date = datetime.now() + timedelta(seconds=10))
    
    scheduler.add_job(
        id = 'run_get_m8u3_4_' + target.stored_filename
      , name = 'video transecoding'
      , func = updateContentsInfo
      , args = (target.stored_filename,)
      , **dynamic_dict
    )
    