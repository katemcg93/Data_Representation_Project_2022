#Flask App for Dog Grooming Site
#Starting with Dog Table

from flask import Flask, jsonify, abort,render_template,url_for, request, redirect, session
import CreateDB
from OwnerDAO import OwnerDAO
from DogDAO import DogDAO
from ServiceDAO import ServiceDAO
from BookingDAO import BookingDAO

app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')
app.secret_key = 'QhGXlgzxcxSdTKGsdfsdfBxUYQd'

dogs = DogDAO().getAll()
services = ServiceDAO().getAll()
owners = OwnerDAO().getAll()
bookings = BookingDAO().getAll()

#Username and password combinations - will need to be logged in to view bookings page
#Need to be logged in as site owner to modify all booking data/services page
user = {
    "katemg93@gmail.com" : "test",
    "emmamurphy@hotmail.com": "test2",
    "siteowner": "test3"
}

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if(request.method == 'POST'):
        username = request.form.get('username')
        password = request.form.get('password')     
        if username in user and password == user[username]:  
            session['username'] = username
            return redirect(url_for('bookings_route'))

        return "<h1>Wrong username or password</h1>"    #if the username or password does not match 

    return render_template("login.html")


#When user logs out - reroute to home page
@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('reroute_home'))
         
@app.route('/dogs', methods = ['GET'])
#If user is siteowner can see all dog details
#Any other logged in user - their dogs only
def getAllDogs():
    if 'username' in session:
        if session['username'] == 'siteowner':
            dogs = DogDAO().getAll()
        else:
            dogs = DogDAO().findByOwnerEmail(session['username'])  
    response = jsonify(dogs)
    #Below is included in functions to stop CORS errors
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/services', methods = ['GET'])
def getAllServices ():
    services = ServiceDAO().getAll()
    response = jsonify(services)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/owners', methods = ['GET'])
def getAllOwners ():
    response = jsonify(owners)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/viewbookings', methods = ['GET'])
#Users forced to log in before seeing this page
#Session details will dictate what data they can see
def bookings_route():
    if not 'username' in session:
        return redirect(url_for('login'))
    else:
        if session['username'] == 'siteowner':
            return render_template('viewbookings.html',loggedInUser = session['username'])
        else:
            ownerdata = OwnerDAO().findByEmail(session['username'])      
        return render_template('viewbookings.html',loggedInUser = ownerdata['first_name'])

@app.route('/viewservices', methods = ['GET'])
def servcies_route():
#If user's not logged in/not site owner - show read only version of page
    if not 'username' in session:
        return render_template("viewservices_readonly.html")
    else:
        if session['username'] == 'siteowner':
            return render_template('viewservices.html', loggedInUser = session['username'])
        else:
            ownerdata = OwnerDAO().findByEmail(session['username'])
            return render_template("viewservices_readonly.html",loggedInUser = ownerdata['first_name'] )

@app.route('/viewservices_readonly', methods = ['GET'])
def services_route_readonly():
    return render_template('viewservices_readonly.html')

@app.route('/bookings', methods = ['GET', 'POST'])
def getAllBookings ():
    if 'username' in session:
        if session['username'] == 'siteowner':
            bookings = BookingDAO().getAll()
        else:
            bookings = BookingDAO().getBookingsForUser(session['username'])
        for i in bookings:
            #Can't parse date-time to JSON - need to convert to string first
            i["date"] = str(i["date"])
            i["time"] = str(i["time"])
        response = jsonify(bookings)
        response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/newbooking/<dog>/<date>/<time>/<servicename>', methods = ['POST'])
def newBooking(dog,date,time,servicename):

    # Need to get service/dog IDS rather than names to booking table
    ServiceID = ServiceDAO().findByName(servicename)
    DogID = DogDAO().findByName(dog)
    values = (date,time,DogID,ServiceID)
    response = jsonify(BookingDAO().create(values))
    return response

@app.route('/deletebooking/<id>', methods = ['DELETE'])
def deleteBooking(id):
    response = jsonify("ok")
    response.headers.add('Access-Control-Allow-Origin', '*')
    BookingDAO().cancelBooking(id)
    return response

@app.route('/deleteservice/<id>', methods = ['DELETE'])
def deleteService(id):
    response = jsonify("ok")
    response.headers.add('Access-Control-Allow-Origin', '*')
    ServiceDAO().delete(id)
    return response

@app.route('/home', methods = ['GET'])
def reroute_home ():
    if 'username' in session:
        #Pass logged in user to page so we know whether to display login/logout option
        return render_template('home.html', loggedInUser = session['username'])
    else:
        return render_template('home.html')


@app.route('/', methods = ['GET'])
def redirect_home ():
    return redirect(url_for('reroute_home'))

@app.route('/updateservice/<id>/<price>/<name>', methods = ['GET','POST'])
def newService(id,name,price):
    values = (name,price,id)
    response = jsonify(values)
    response.headers.add('Access-Control-Allow-Origin', '*')
    ServiceDAO().update(values)
    return response

@app.route('/createservice/<price>/<name>', methods = ['GET','POST'])
def updateService (name,price):
    values = (name,price)
    response = jsonify(values)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response = jsonify(ServiceDAO().create(values))
    return response


@app.route('/updatebooking/<id>/<date>/<time>/<servicename>', methods = ['GET','POST'])
def updateBooking(id,date,time,servicename):
    serviceid = ServiceDAO().findByName(servicename)
    response = jsonify(date,time,serviceid)
    response.headers.add('Access-Control-Allow-Origin', '*')
    values = (date,time,serviceid,id)
    BookingDAO().update(values)

    return response

if __name__ == "__main__":
    app.run(debug=True)