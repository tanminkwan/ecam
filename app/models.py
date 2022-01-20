from flask import Markup, url_for
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import FileColumn
from sqlalchemy import Table, Column, Integer, String, Text, ForeignKey, DateTime, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from .common import get_user, get_hostname, YnEnum
from . import app

"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who

"""

class ContentMaster(Model):

    __tablename__ = "content_master"
    __table_args__ = {"comment":"Content 정보"}
    
    id = Column(Integer, primary_key=True)
    filename        = Column(String(100), nullable=False, comment='컨텐츠 파일 이름')
    stored_filename = Column(String(500), nullable=False, comment='등록된 파일 이름')
    description     = Column(String(500), nullable=True, comment='설명')
    content_type    = Column(String(50), nullable=True, comment='컨텐츠 파일 Type')
    manifest_path   = Column(String(500), nullable=True, comment='m8u3 파일 url path')
    ref_stored_filename = Column(String(500), nullable=True, comment='참조하는 파일 이름')
    valid_yn        = Column(Enum(YnEnum), info={'enum_class':YnEnum}, comment='파일 유효성 여부')
    hostname        = Column(String(200), default=get_hostname, nullable=False, comment='입력 서버')
    user_id         = Column(String(100), default=get_user, nullable=False, comment='입력 user')
    create_on       = Column(DateTime(), default=datetime.now, nullable=False, comment='입력 일시')
    
    UniqueConstraint(stored_filename)
    
    def stream_url(self):
        return app.config['STREAM_URL'] if self.valid_yn is not None and self.valid_yn.name == 'YES' else ''
    
    def __repr__(self):
        return self.filename

assoc_program_contentmaster = Table('ref_program_contentmaster', Model.metadata,
                                    Column('id', Integer, primary_key=True),
                                    Column('id_of_program', Integer, ForeignKey('program.id', ondelete='CASCADE')),
                                    Column('id_of_contentmaster', Integer, ForeignKey('content_master.id', ondelete='CASCADE'))
                                    )

class Program(Model):

    __tablename__ = "program"
    __table_args__ = {"comment":"교육 과정"}
    
    id = Column(Integer, primary_key=True)
    program_name    = Column(String(200), nullable=False, comment='교육 과정 이름')
    description     = Column(Text, nullable=True, comment='설명')
    author          = Column(String(100), nullable=True, comment='작성자')
    hostname        = Column(String(200), default=get_hostname, nullable=False, comment='입력 서버')
    user_id         = Column(String(100), default=get_user, nullable=False, comment='입력 user')
    create_on       = Column(DateTime(), default=datetime.now, nullable=False, comment='입력 일시')

    content_master  = relationship('ContentMaster', secondary=assoc_program_contentmaster, backref='program')
    
    def contentmaster(self):
        contents = []
        for row in self.content_master:
            contents.append(row.id)
        return contents
        
    def __repr__(self):
        return self.program_name

class TestTable(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(500), nullable=True)
    create_on = Column(DateTime(), default=datetime.now, nullable=False)

    def __repr__(self):
        return self.name

class EcamFile(Model):
    __tablename__ = "ecam_file"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(500), nullable=True)
    file = Column(FileColumn, nullable=False)
    create_on = Column(DateTime(), default=datetime.now, nullable=False)

    def type_t(self):

        file_type = str(self.file).split('.')[-1:][0].upper()

        if file_type == 'MP4':
            html_t = "<button type=\"button\" onclick=\"location.href=\'"
            html_t = html_t + '/teststream/stream/' + str(self.file)
            html_t = html_t + "\'\">" + file_type + "</button>"
        elif file_type == 'JPG':
            html_t = "<button type=\"button\" onclick=\"location.href=\'"
            html_t = html_t + '/teststream/image/' + str(self.file)
            html_t = html_t + "\'\">" + file_type + "</button>"
        else:
            html_t = "<p>" + file_type + "</p>"

        return Markup(html_t)

    def download(self):
        return Markup(
                '<a href="'
                + url_for("EcamFileView.download", filename=str(self.file))
                + '">Download</a>'
                )

    def __repr__(self):
        return self.name
