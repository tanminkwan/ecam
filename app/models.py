from flask import Markup, url_for
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import FileColumn
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who


"""
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
