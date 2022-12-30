import mysql.connector
import dbconfig2 as cfg
import CreateDB

class OwnerDAO:
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
        sql="insert into customer (first_name,last_name,email, phone) values (%s,%s,%s,%s)"
        cursor.execute(sql, values)

        self.connection.commit()
        newid = cursor.lastrowid
        self.closeAll()
        return newid

    def getAll(self):
        cursor = self.getcursor()
        sql="select * from customer"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        for result in results:
            returnArray.append(self.convertToDictionary(result))
        
        self.closeAll()
        return returnArray

    def findByID(self, id):
        cursor = self.getcursor()
        sql="select * from customer where id = %s"
        values = (id,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        returnvalue = self.convertToDictionary(result)
        self.closeAll()
        return returnvalue
       
    def findByEmail(self, email):
        cursor = self.getcursor()
        sql="select * from customer where email = %s"
        values = (email,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        returnvalue = self.convertToDictionary(result)
        self.closeAll()
        return returnvalue

    def update(self, values):
        cursor = self.getcursor()
        sql="update customer set email= %s, phone=%s where id = %s"
        cursor.execute(sql, values)
        self.connection.commit()
        self.closeAll()
        
    def delete(self, id):
        cursor = self.getcursor()
        sql="delete from customer where id = %s"
        values = (id,)

        cursor.execute(sql, values)

        self.db.commit()
        self.closeAll()
        
        print("delete done")

    def convertToDictionary(self, result):
        colnames=['id','first_name','last_name','email', 'phone']
        item = {}
        
        if result:
            for i, colName in enumerate(colnames):
                value = result[i]
                item[colName] = value
        
        return item
    
data = [('Kate', 'McGrath', 'katemg93@gmail.com', '0879512511'), ('Emma', 'Murphy', 'emmamurphy@hotmail.com', '0879413256')]

        
ownerDAO = OwnerDAO()


if __name__ == "__main__":
    for x in data:
        ownerDAO.create(x)
    print(ownerDAO.getAll())
