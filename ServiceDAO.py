import mysql.connector
import dbconfig2 as cfg
import CreateDB

class ServiceDAO:
    connection=""
    cursor =''
    host=       ''
    user=       ''
    password=   ''
    database=   ''
    
    def __init__(self):
        self.host=       cfg.mysql['host']
        self.user=       cfg.mysql['user']
        self.password=   cfg.mysql['password']
        self.database=   'groomer'

    def getcursor(self): 
        self.connection = mysql.connector.connect(
            host=       self.host,
            user=       self.user,
            password=   self.password,
            database=   self.database,
        )
        self.cursor = self.connection.cursor()
        return self.cursor

    def closeAll(self):
        self.connection.close()
        self.cursor.close()
         
    def create(self, values):
        cursor = self.getcursor()
        sql="insert into service (name,price) values (%s,%s)"
        cursor.execute(sql, values)

        self.connection.commit()
        newid = cursor.lastrowid
        self.closeAll()
        return newid

    def getAll(self):
        cursor = self.getcursor()
        sql="select * from service"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        for result in results:
            returnArray.append(self.convertToDictionary(result))
        
        self.closeAll()
        return returnArray

    def findByID(self, id):
        cursor = self.getcursor()
        sql="select * from service where id = %s"
        values = (id,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        returnvalue = self.convertToDictionary(result)
        self.closeAll()
        return returnvalue
    
    def findByName(self, name):
        cursor = self.getcursor()
        sql="select id from service where name = %s"
        values = (name,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        item = {}
        item["id"] = result
        return result[0]

    def update(self, values):
        cursor = self.getcursor()
        sql="update service set name= %s, price=%s where id = %s"
        cursor.execute(sql, values)
        self.connection.commit()
        self.closeAll()
        
    def delete(self, id):
        cursor = self.getcursor()
        sql="delete from service where id = %s"
        values = (id,)
        cursor.execute(sql, values)
        self.connection.commit()
        self.closeAll()
        
        print("delete done")

    def convertToDictionary(self, result):
        colnames=['id','name','price']
        item = {}
        
        if result:
            for i, colName in enumerate(colnames):
                value = result[i]
                item[colName] = value
        
        return item
        
serviceDAO = ServiceDAO()
data = [ ('Full Groom', '50.00'), ('Wash and Blow Dry', '25.00'), ('De-Shed', '60.00'), ('Nails and Ears', '20.00')]

if __name__ == "__main__":
    for x in data:
        serviceDAO.create(x)
