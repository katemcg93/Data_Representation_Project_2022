# Data Representation Project 2022

### Name : Kate McGrath
### Student Number : G00398908
### Submission Date : 31/12/2022

### Getting Started
#### Packages
The following packages are required to run the site on your local machine:
 - Flask==1.1.2
 - mysql_connector_repackaged==0.3.1
These can also be found in the requirements.txt file in this repository.

#### MySQL Connector
The database configuration details are passed from the dbconfig2.py file to the Flask app. The version of this file on Github is a template, and the host/user/password details should be updated before attempting to run the app.

#### PythonAnywhere
This site is hosted on PythonAnywhere at the below link:

https://katemcg93.pythonanywhere.com

### Overview of Site
#### Database Objects
 This site represents a dog grooming business and consists of the following main objects: 
  - Services: Types of treatments offered and prices
  - Owners: Customers who may own one or more dogs, who can be booked for treatments
  - Dogs: Connected to Owners - details stored include name, age and breed of dog
  - Appointments: Include date/time, dog and treatment
  
#### Site Pages
  The site includes the following main pages:
  - Home
  - Login
  - Services
  - Bookings
  
  On the Service and Booking pages, the following actions are possible:
  - Create/Modify/Delete Booking
  - Create/Modify/Delete Service
  
  ### User Details
On the login page, the user is asked to enter their username and password, which is checked against a dictionary object called user in the flask_app file. The program first checks if the username is in the dictionary, then if the password is a match ,if so the user is authenticated and a session is initiated.

There are three potential username/password combinations. The first two correspond to entries in the Owner database table, and the third is for the site owner, providing full edit access on all objects within the site.

1. Username : katemg93@gmail.com, Password: test
2. Username : emmamurphy@hotmail.com, Password: test2
3. Username : siteowner, Password: test3

The site behaviour/pages displayed depends on current session data:
  - Users must be logged in to see the bookings page. Users can only view/create bookings for their own dogs. The site owner can modify all 
  - If the logged in user is the site owner, they will have full CRUD access on the service object. Regular/unregistered users will be redirected to a read-only version of the services page.
 - If a user is logged in, a welcome message will be displayed in the nav bar. For the two standard users, their first name will be displayed (taken from the Owner DB table), whereas for the site owner, their username is displayed.
 
 
