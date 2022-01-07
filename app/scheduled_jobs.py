from . import db, scheduler
from .batchs import batch_transVideos

@scheduler.task('cron', id='job_transVideos', name='Auto Transcoding Videos', minute='*/1')
def job_transVideos():
    batch_transVideos()