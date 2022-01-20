from . import db, app
from .queries import selectRows, updateRows

from datetime import datetime, timedelta
import os

def batch_transVideos():
    
    print('batch_transVideos : ', datetime.now())
    
def updateContentsInfo(stored_filename):
    
    if _isStreamValid(stored_filename):
        valid_yn = 'YES'
        manifest_path, content_type = _getManifestPath(stored_filename)
    else:
        valid_yn = 'NO'
        manifest_path, content_type = '', ''
        
    update_dict = dict(
        valid_yn      = valid_yn
      , manifest_path = manifest_path
      , content_type  = content_type
    )
    
    filter_dict = dict(
        stored_filename = stored_filename
    )    
    
    updateRows('content_master', update_dict, filter_dict)
    
    db.session.commit()
    
def _isStreamValid(stored_filename):
    
    fullfilename = app.config['IMG_UPLOAD_URL'] + stored_filename
    
    return os.path.isfile(fullfilename)

def _getManifestPath(stored_filename):
    
    filetype = stored_filename.split('.')[-1].lower()
    
    if filetype in ['mp4','mov']:
        manifest_path = '/contents/' + stored_filename + '/playlist.m3u8'
    elif filetype in ['jpg','png','gif']:
        manifest_path = '/images/' + stored_filename
    else:
        manifest_path = ''
        
    return manifest_path, filetype
