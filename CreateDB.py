import mysql.connector
import dbconfig2 as cfg

db = mysql.connector.connect(
  host= cfg.mysql['host'],
  user= cfg.mysql['user'],
  password= cfg.mysql['password']
)

cursor = db.cursor()

# Create DB if required and use it
cursor.execute("create DATABASE IF NOT EXISTS groomer")
db.database = 'groomer'

cursor.execute("create TABLE IF NOT EXISTS customer (id INT AUTO_INCREMENT PRIMARY KEY, first_name VARCHAR (250), last_name VARCHAR (250), email VARCHAR(250), phone CHAR (10))")
cursor.execute("create TABLE IF NOT EXISTS dog (id INT AUTO_INCREMENT PRIMARY KEY,OwnerID int NOT NULL, FOREIGN KEY(OwnerID) REFERENCES customer(id), name VARCHAR(250), age INT, breed VARCHAR(250))")
cursor.execute("create TABLE IF NOT EXISTS service (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR (250), price VARCHAR(250))")
cursor.execute("create TABLE IF NOT EXISTS booking (id INT AUTO_INCREMENT PRIMARY KEY, date DATE, time TIME, DogID int NOT NULL, ServiceID int NOT NULL, FOREIGN KEY(DogID) REFERENCES dog(id),FOREIGN KEY(ServiceID) REFERENCES service(id))")

print(db.database)
db.close()
cursor.close()






