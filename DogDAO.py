import mysql.connector
import dbconfig2 as cfg
import CreateDB

class DogDAO:
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
        sql="insert into dog (OwnerId,name,age, breed) values (%s,%s,%s,%s)"
        cursor.execute(sql, values)

        self.connection.commit()
        newid = cursor.lastrowid
        self.closeAll()
        return newid

    def findByName(self, name):
        cursor = self.getcursor()
        sql="select id from dog where name = %s"
        values = (name,)
        cursor.execute(sql, values)
        result = cursor.fetchone()
        item = {}
        item["id"] = result
        return result[0]
    
    def findByOwnerEmail(self,email):
        cursor = self.getcursor()
        sql="select CONCAT(c.first_name,Char(32),c.last_name) as Owner, d.name, d.age, d.breed from dog d inner join customer c on c.id = d.OwnerID where c.email = %s"
        values = (email,)
        cursor.execute(sql,values)
        results = cursor.fetchall()
        returnArray = []
        print(results)
        for result in results:
            print(result)
            returnArray.append(self.convertToDictionary(result))
        self.closeAll()
        return returnArray


    def getAll(self):
        cursor = self.getcursor()
        sql="select CONCAT(c.first_name,Char(32),c.last_name) as Owner, d.name, d.age, d.breed from dog d inner join customer c on c.id = d.OwnerID"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        print(results)
        for result in results:
            print(result)
            returnArray.append(self.convertToDictionary(result))
        
        self.closeAll()
        return returnArray

    def findByID(self, id):
        cursor = self.getcursor()
        sql="select * from dog where id = %s"
        values = (id,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        returnvalue = self.convertToDictionary(result)
        self.closeAll()
        return returnvalue

    def update(self, values):
        cursor = self.getcursor()
        sql="update dog set name= %s, age=%s , breed=%s where id = %s"
        cursor.execute(sql, values)
        self.connection.commit()
        self.closeAll()
        
    def delete(self, id):
        cursor = self.getcursor()
        sql="delete from dog where id = %s"
        values = (id,)

        cursor.execute(sql, values)

        self.db.commit()
        self.closeAll()
        
        print("delete done")

    def convertToDictionary(self, result):
        colnames=['Owner','name','age', 'breed']
        item = {}
        
        if result:
            for i, colName in enumerate(colnames):
                value = result[i]
                item[colName] = value
        
        return item
        
dogDAO = DogDAO()
values = [ ('2', 'Holly', '1', 'Cocker Spaniel'), ('1', 'Jack', '3', 'Labrador'), ('2', 'Charlie', '2', 'Dachshund'), ('1', 'Penny', '10', 'Cockapoo')]
if __name__ == "__main__":
    for x in values:
        dogDAO.create(x)
    print(dogDAO.getAll())
