from . import db

table_dict = {table.__tablename__: table for table in db.Model.__subclasses__()}
table_args = {table.__tablename__: table.__table_args__ for table in db.Model.__subclasses__()}

def getAllTables():
    
    return [ t for t in table_dict ]

def selectRow(table_name, filter_dict):
    
    filter_list = []
    table = _getTableOjbect(table_name)
    if not table:
        return None, -1
    
    for item in filter_dict:
        col = getattr(table, item)
        filter_list.append(col==filter_dict[item])
        
    rec = db.session.query(table)\
        .filter(*filter_list).first()
        
    return rec, 1

def selectRows(table_name, filter_dict):
    
    filter_list = []
    table = _getTableOjbect(table_name)
    
    for item in filter_dict:
        col = getattr(table, item)
        filter_list.append(col==filter_dict[item])
        
    recs = db.session.query(table)\
        .filter(*filter_list).all()
        
    return recs, 1

def updateRows(table_name, update_dict, filter_dict):
    
    filter_list = []
    table = _getTableOjbect(table_name)
    
    for item in filter_dict:
        col = getattr(table, item)
        filter_list.append(col==filter_dict[item])
        
    rt = db.session.query(table)\
        .filter(*filter_list)\
        .update(update_dict)
        
    if rt < 1:
        return -1, table_name + ' data to update isn\'t found : '
    return 1, ''

def _getTableOjbect(table_name):
    return next((t for t in db.Model.__subclasses__() if t.__tablename__ == table_name), None)
    