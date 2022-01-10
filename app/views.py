from flask import render_template, request, Response, send_file, jsonify
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import BaseView, ModelView, ModelRestApi, has_access
from flask_appbuilder.filemanager import FileManager, uuid_namegen
from flask_appbuilder.api import BaseApi, expose, protect
from .models import ContentMaster, TestTable, EcamFile
from . import appbuilder, db, app

import os
import re
import json

"""
    Create your Model based REST API::

    class MyModelApi(ModelRestApi):
        datamodel = SQLAInterface(MyModel)

    appbuilder.add_api(MyModelApi)


    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::


    appbuilder.add_view(
        MyModelView,
        "My View",
        icon="fa-folder-open-o",
        category="My Category",
        category_icon='fa-envelope'
    )
"""

class TestTableView(ModelView):
    datamodel = SQLAInterface(TestTable)
    list_title = 'CRUD TEST'
    list_columns = ['id','name','description','create_on']
    label_columns = {'id':'SEQ','name':'이름','description':'메세지','create_on':'생성일지'}
    edit_exclude_columns = ['id','create_on']
    add_exclude_columns = ['id','create_on']

class TestTableApi(ModelRestApi):
    
    datamodel = SQLAInterface(TestTable)

class EcamFileView(ModelView):
    datamodel = SQLAInterface(EcamFile)
    list_title = 'File Upload TEST'
    list_columns = ['id','type_t', 'name','description','download','create_on']
    label_columns = {'id':'SEQ','type_t':'파일Type','name':'이름','description':'메세지','create_on':'생성일지'}
    edit_exclude_columns = ['id','create_on']
    add_exclude_columns = ['id','create_on']

class ContentMasterApi(ModelRestApi):
    
    datamodel = SQLAInterface(ContentMaster)

class ContentsManager(BaseApi):
    
    resource_name = 'contents'
    
    @expose('/video', methods=['POST'])
    @protect()
    def post_video(self, **kwargs):
        """POST Vidoe Upload
        ---
        post:
          description: Upload a video file
          requestBody:
            description: Video file
            required: true
            content:
              multipart/form-data:
                schema:
                  type: object
                  properties:
                    file:
                      type: string
                      format: binary
          responses:
            201:
              description: File Uploaded
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      return_code:
                        type: integer
                      stored_file_name:
                        type: string
                      message:
                        type: string
                    example:
                      return_code: 1
                      stored_file_name: f70c9a39-6f88-11ec-9c34-00505694d9ee_sep_file_example.mp4
                      message: Well done
            415:
              description: Invalid Video Type
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      return_code:
                        type: integer
                      message:
                        type: string
                    example:
                      return_code: -1
                      message: jpg is not a video type.
        """
        file = request.files['file']
        filetype = file.filename.split('.')[-1]
        
        if filetype.lower() not in ['mp4','mov']:
            return jsonify({'return_code':-1, 'message':filetype+' is not a video type.'}), 415
        
        fm = FileManager()        
        
        sfilename = fm.save_file(file, uuid_namegen(file))
        
        return jsonify({'return_code':1, 'stored_file_name':sfilename, 'message':'well done'}), 201
        
    
class TestStream(BaseView):

    default_view = 'stream'

    def get_chunk(self, file_name, byte1=None, byte2=None):
        print("HHH : ", app.root_path, file_name)
        full_path = "/static/uploads/" + file_name
        file_size = os.stat(full_path).st_size
        start = 0

        if byte1 < file_size:
            start = byte1
        if byte2:
            length = byte2 + 1 - byte1
        else:
            length = file_size - start

        with open(full_path, 'rb') as f:
            f.seek(start)
            chunk = f.read(length)

        return chunk, start, length, file_size

    @expose('/stream/')
    def stream(self):
        return 'Hello'

    @expose('/video/<string:param1>')
    @has_access
    def video(self, param1):
        range_header = request.headers.get('Range', None)
        byte1, byte2 = 0, None
        #byte1, byte2 = 0, 1024
        if range_header:
            match = re.search(r'(\d+)-(\d*)', range_header)
            groups = match.groups()

            if groups[0]:
                byte1 = int(groups[0])
            if groups[1]:
                byte2 = int(groups[1])

        chunk, start, length, file_size = self.get_chunk(param1, byte1, byte2)
        resp = Response(chunk, 206, mimetype='video/mp4',
                      content_type='video/mp4', direct_passthrough=True)
        resp.headers.add('Content-Range', 'bytes {0}-{1}/{2}'.format(start, start + length - 1, file_size))
        resp.headers.add('Accept-Ranges', 'bytes')
        return resp

    @expose('/stream/<string:param1>')
    @has_access
    def stream2(self, param1):
        #file_name = "0a81e91c-3307-11ec-b8cf-005056a50b96_sep_20210613_154319.mp4"
        return render_template('my_list.html',file_name='/teststream/video/'+param1, base_template=appbuilder.base_template, appbuilder=appbuilder)

    @expose('/photo/<string:param1>')
    @has_access
    def photo(self, param1):
        full_path = "/static/uploads/" + param1
        return send_file(full_path, mimetype='image/jpg')

    @expose('/image/<string:param1>')
    @has_access
    def image2(self, param1):
        return render_template('my_list2.html',file_name='/teststream/photo/'+param1, base_template=appbuilder.base_template, appbuilder=appbuilder)

"""
    Application wide 404 error handler
"""
@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )

db.create_all()
appbuilder.add_view(
    TestTableView,
    "CRUD Test",
    icon = "fa-folder-open-o",
    category = "TEST MENU",
    category_icon = "fa-envelope"
)
appbuilder.add_view(
    EcamFileView,
    "File Up/Down",
    icon = "fa-folder-open-o",
    category = "TEST MENU"
)
appbuilder.add_view_no_menu(TestStream, "stream")
appbuilder.add_api(TestTableApi)
appbuilder.add_api(ContentsManager)
appbuilder.add_api(ContentMasterApi)