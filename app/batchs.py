from . import db, app
from .queries import selectRows, updateRows

from datetime import datetime, timedelta
import os

def batch_transVideos():
    
    print('batch_transVideos : ', datetime.now())
    
def updateContentsInfo(stored_filename):

    manifest_path, file_type, content_type, fullfilename\
        = _getManifestPath(stored_filename)
    
    if _isStreamValid(fullfilename):
        valid_yn = 'YES'
    else:
        valid_yn = 'NO'
        manifest_path, file_type, content_type = '', '', ''
        
    update_dict = dict(
        valid_yn      = valid_yn
      , manifest_path = manifest_path
      , file_type     = file_type
      , content_type  = content_type
    )
    
    filter_dict = dict(
        stored_filename = stored_filename
    )    
    
    updateRows('content_master', update_dict, filter_dict)
    
    db.session.commit()
    
def _isStreamValid(fullfilename):
    
    return os.path.isfile(fullfilename)

def _getManifestPath(stored_filename):
    
    filetype = stored_filename.split('.')[-1].lower()
    
    if filetype in ['mp4','mov']:
        manifest_path = '/contents/' + stored_filename + '/playlist.m3u8'
        fullfilename = app.config['UPLOAD_FOLDER'] + stored_filename
        contentType = 'video'
    elif filetype in ['jpg','jpeg','png','gif']:
        manifest_path = '/images/' + stored_filename
        fullfilename = app.config['IMG_UPLOAD_FOLDER'] + stored_filename
        contentType = 'image'
    else:
        manifest_path = ''
        fullfilename = ''
        contentType = ''
        
    return manifest_path, filetype, contentType, fullfilename
