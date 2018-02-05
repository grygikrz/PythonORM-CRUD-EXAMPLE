import os


from sqlalchemy import Column, DateTime, String, Integer, Float, ForeignKey, func
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


Base = declarative_base()


class Restaurant(Base):
    __tablename__ = 'restaurant'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable = False)

class MenuItem(Base):
    __tablename__ = 'menuitem'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable = False)
    description = Column(String)
    price = Column(String(8))
    course = Column(String)
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))

    """ delete,all used for cascade deletion"""
    restaurant = relationship(Restaurant,
                                backref = backref('menuitem',
                                                uselist=True,
                                                cascade = 'delete,all'))


engine = create_engine('sqlite:///restaurant.db')

Session  = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

session = Session()


#append to page HTML
def getData(table):
    session = Session()
    data = session.query(Base.metadata.tables[table]).all()

    main_page = '<html><head><link rel="icon" href="data:;base64,iVBORw0KGgo="></head><body>'
    main_page += '''<a href="http://127.0.0.1:8000/restaurant"> Restaurant</a><br><a href="http://127.0.0.1:8000/menuitem"> Menu Item</a><br><form method='POST' enctype='multipart/form-data' action='/add/{table}'><h2>Add new item to the list</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''.format(table=table)
    main_page += '<ul>'

    for value in data:
        main_page += '<li>{value}<a href="/edit/{table}/{itemNumber}">  Edit</a><a href=/delete/{table}/{itemNumber}> Delete</a></li>'.format(value=value.name,table=table,itemNumber=value.id)

    main_page += '</ul></body></html>'

    return main_page


def createData(table,datas):
    session = Session()
    data = Base.metadata.tables[table]
    session.execute(data.insert(),{'name':datas})
    session.commit()
    return '''<html><head><link rel="icon" href="data:;base64,iVBORw0KGgo=">
            </head><body>New item added!. <a href="http://127.0.0.1:8000/{table}"> Back to list</a></body></html>'''.format(table=table)


def getOneData(table,idNumber):
    session = Session()
    data = Base.metadata.tables[table]
    id = data.c.id
    data = session.query(data).filter_by(id=int(idNumber)).one()
    page = """<html><head><link rel="icon" href="data:;base64,iVBORw0KGgo="></head><body><form method='POST' enctype='multipart/form-data' action=''><h2>Tell me. Edit item:</h2><input name="message" type="text" value="{datas}" ><input type="submit" value="Submit"> </form></body></html>""".format(datas=data.name)
    return page


def delData(table,idNumber):
    session = Session()

    data = Base.metadata.tables[table]
    session.execute(data.delete().where(data.c.id==int(idNumber)))
    session.commit()
    #data = session.data.filter(id==int(idNumber))
    #session.delete(data)
    #session.commit()
    return '''<html><head><link rel="icon" href="data:;base64,iVBORw0KGgo=">
            </head><body>Item deleted.<a href="http://127.0.0.1:8000/{table}"> Back to list</a></body></html>'''.format(table=table)


def updateData(table,idNumber,datas):
    session = Session()
    data = Base.metadata.tables[table]
    name = data.c.name
    id = data.c.id
    session.execute(data.update().where(id==int(idNumber)).values(name=datas))
    session.commit()
    return '''<html><head><link rel="icon" href="data:;base64,iVBORw0KGgo=">
            </head><body>Item updated! <a href="http://127.0.0.1:8000/{table}">Back to list</a></body></html>'''.format(table=table)
