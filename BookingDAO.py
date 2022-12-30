import mysql.connector
import dbconfig2 as cfg
import CreateDB

class BookingDAO:
    connection=""
    cursor =    ''
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
        sql="insert into booking (date,time,DogID,ServiceID) values (%s,%s, %s, %s)"
        cursor.execute(sql, values)

        self.connection.commit()
        newid = cursor.lastrowid
        self.closeAll()
        return newid

    def getAll(self):
        cursor = self.getcursor() 
        sql="select b.id, d.name,  b.ServiceID,s.name, b.date, b.time, c.id from booking b inner join dog d on d.id = b.DogId inner join service s on s.id = b.ServiceID inner join customer c on c.id = d.OwnerID;"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        for result in results:
            returnArray.append(self.convertToDictionary(result))
        
        self.closeAll()
        return returnArray
    
    def getBookingsForUser(self,email):
        cursor = self.getcursor() 
        sql="select b.id, d.name, b.ServiceID,s.name, b.date, b.time, c.id from booking b inner join dog d on d.id = b.DogId inner join service s on s.ID = b.ServiceID inner join customer c on d.OwnerID = c.ID where c.email = %s;"
        values = (email,)
        cursor.execute(sql,values)
        results = cursor.fetchall()
        returnArray = []
        for result in results:
            returnArray.append(self.convertToDictionary(result))
        
        self.closeAll()
        return returnArray
    

    def findByID(self, id):
        cursor = self.getcursor()
        sql="select b.id, d.name, b.ServiceID,s.name, b.date, b.time, c.firstname from booking b inner join dog d on d.id = b.DogId inner join service s on s.id = b.ServiceID inner join customer c on c.id = d.OwnerID where b.id = %s;"
        values = (id,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        returnvalue = self.convertToDictionary(result)
        self.closeAll()
        return returnvalue

    def update(self, values):
        cursor = self.getcursor()
        sql="update booking set date= %s, time = %s, ServiceID = %s where id = %s"
        cursor.execute(sql, values)
        self.connection.commit()
        self.closeAll()
        
    def cancelBooking(self, id):
        cursor = self.getcursor()
        sql="delete from booking where id = %s"
        values = (id,)

        cursor.execute(sql, values)

        self.connection.commit()
        self.closeAll()
        
        print("delete done")

    def convertToDictionary(self, result):
        colnames=['id','Dog','ServiceID','Service','date', 'time','OwnerID']
        item = {}
        
        if result:
            for i, colName in enumerate(colnames):
                value = result[i]
                item[colName] = value
        
        return item
        
bookingDAO = BookingDAO()

data = [('2022-12-23', '14:30:00', '1', '3'),('2022-12-20', '11:30:00', '3', '4'), ('2022-12-18', '14:00:00', '4', '2'), ('2022-12-18', '14:00:00', '2', '3')]

if __name__ == "__main__":
    email = "katemg93@gmail.com"
    print(bookingDAO.getBookingsForUser(email))
