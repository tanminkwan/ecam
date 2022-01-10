from . import db

table_dict = {table.__tablename__: table for table in db.Model.__subclasses__()}
table_args = {table.__tablename__: table.__table_args__ for table in db.Model.__subclasses__()}

def getAllTables():
    
    return [ t for t in table_dict ]

def selectRow(table_name, filter_dict):
    
    filter_list = []
    table = table_dict[table_name]
    
    for item in filter_dict:
        col = getattr(table, item)
        filter_list.append(col==filter_dict[item])
        
    rec = db.session.query(table)\
        .filter(*filter_list).first()
        
    return rec, 1

def selectRows(table_name, filter_dict):
    
    filter_list = []
    table = table_dict[table_name]
    
    for item in filter_dict:
        col = getattr(table, item)
        filter_list.append(col==filter_dict[item])
        
    recs = db.session.query(table)\
        .filter(*filter_list).all()
        
    return recs, 1

