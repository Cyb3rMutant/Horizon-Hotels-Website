# purpose:  A website for a hotel
# module: Web Development and Databases
# author: Yazeed Abu-Hummos
# UWE ID: 21014295
# last edit time and date: 05:51 30/04/2022


from flask import Flask, request, render_template, send_file, url_for, redirect, session
import dbfunc
from datetime import datetime, date, timedelta
from passlib.hash import sha256_crypt
import os
app = Flask(__name__)
app.secret_key = "a1V#9R^l6vhGI'Xyms@]ARPJ"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
currencies = {}


def get_cur():
    global currencies
    conn = dbfunc.getConnection()  # connection to DB
    dbcursor = conn.cursor()  # Creating cursor object
    dbcursor.execute("SELECT * FROM CURRENCY_CONV;")
    rows = dbcursor.fetchall()
    currencies = {}
    for cur in rows:
        currencies[cur[0]] = cur[1]
    dbcursor.close()
    conn.close()  # Conne


@app.route("/")
@app.route("/home", methods=["GET", "POST"])
def index():
    if "rid" in session:
        os.remove(os.path.join(app.root_path, "receipts",
                  "booking%s.txt" % session["rid"]))
        session.pop("rid")
    conn = dbfunc.getConnection()  # connection to DB
    if conn != None:  # Checking if connection is None
        if conn.is_connected():
            dbcursor = conn.cursor()  # Creating cursor object
            if not len(currencies):
                get_cur()
            if "currency" not in session:
                get_cur()
                session["currency"] = "GBP"
            dbcursor.execute(
                "SELECT MIN(PriceOffPeak*(1+(SELECT MIN(PricePercentage) FROM ROOMS))),\
                MAX(PricePeak*(1+(SELECT MAX(PricePercentage) FROM ROOMS))),MIN(MaxCapacity),MAX(MaxCapacity) FROM HOTELS,ROOMS;"
            )
            intervals = dbcursor.fetchone()
            if request.method == "POST":
                if request.form["formType"] == "currency":
                    session["currency"] = request.form["currency"]
                if request.form["formType"] == "filter":
                    maxprice = request.form["max"]
                    minprice = request.form["min"]
                    people = request.form["people"]
                    search = request.form["search"]
                    start = request.form["from"]
                    end = request.form["to"]
                    dbcursor.execute(
                        'SELECT h.HotelLocation as hotel, r.RoomType as type, \
                        FLOOR(IF(%s BETWEEN 4 AND 9, h.PricePeak, h.PriceOffPeak)*(1+r.PricePercentage+(r.ExtraPriceForGuest*%s))) as price,\
                        r.MaxCapacity, Description, FLOOR(h.NumberOfRooms*r.PercentageOfRooms) as m, \
                        (SELECT COUNT(*) FROM `RESERVATIONS` re \
                        WHERE re.Cancelled=false AND h.HotelLocation=re.HotelLocation AND r.RoomType=re.RoomType AND \
                        ((re.StartDate BETWEEN "{start}" AND "{end}") OR ("{start}" BETWEEN re.StartDate AND re.EndDate))) as c \
                        FROM HOTELS h CROSS JOIN ROOMS r \
                        WHERE r.MaxCapacity>=%s\
                        HAVING hotel LIKE "%{srch}%" AND (price BETWEEN %s/{cur} AND %s/{cur}) AND c<m \
                        ORDER BY hotel, price;'.format(srch=search, start=start, end=end, cur=currencies[session["currency"]]),
                        (datetime.strptime(request.form["from"], "%Y-%m-%d").month, int(people) - 1, people, minprice, maxprice,),)
                    rows = dbcursor.fetchall()
                    hotels = {}
                    for prod in rows:
                        if (prod[0], prod[4]) in hotels:
                            hotels[(prod[0], prod[4])][prod[1]] = [
                                prod[2], prod[3]]
                        else:
                            hotels[(prod[0], prod[4])] = {
                                prod[1]: [prod[2], prod[3]]}
                    dbcursor.execute(
                        'SELECT h.HotelLocation as hotel, Description, IF(%s BETWEEN 4 AND 9, h.PricePeak, h.PriceOffPeak) as price,  \
                        h.NumberOfRooms as m, \
                        (SELECT COUNT(*) FROM `RESERVATIONS` re \
                        WHERE re.Cancelled=false AND h.HotelLocation=re.HotelLocation AND \
                        ((re.StartDate BETWEEN "{start}" AND "{end}") OR ("{start}" BETWEEN re.StartDate AND re.EndDate))) as c \
                        FROM HOTELS h \
                        HAVING hotel LIKE "%{srch}%" AND \
                        ((SELECT PricePercentage FROM ROOMS WHERE (price*(1+PricePercentage)) BETWEEN %s AND %s LIMIT 1) IS NOT NULL) AND  c>=m \
                        ORDER BY hotel;'.format(srch=search, start=start, end=end), (datetime.strptime(request.form["from"], "%Y-%m-%d").month, minprice, maxprice,),)
                    rows = dbcursor.fetchall()
                    for hotel in rows[::-1]:
                        if (hotel[0], hotel[1]) in hotels:
                            rows.remove(hotel)
                    return render_template("home_page.html", hotels=hotels, loggedin="logged_in" in session, currencies=currencies, admin="logged_in" in session and "@hhotels.co.uk" in session["email"], currentCurrency=session["currency"], fullybooked=rows, intervals=intervals, fromdate=start, todate=end,)
            months = date.today().month
            start = date.today()+timedelta(days=1)
            end = date.today() + timedelta(days=2)
            dbcursor.execute(
                'SELECT h.HotelLocation as hotel, r.RoomType as type, \
                FLOOR(IF(%s BETWEEN 4 AND 9, h.PricePeak, h.PriceOffPeak)*(1+r.PricePercentage)) as price, \
                r.MaxCapacity, Description, FLOOR(h.NumberOfRooms*r.PercentageOfRooms) as m, \
                (SELECT COUNT(*) FROM `RESERVATIONS` re \
                WHERE re.Cancelled=false AND h.HotelLocation=re.HotelLocation AND r.RoomType=re.RoomType AND \
                ((re.StartDate BETWEEN "{start}" AND "{end}") OR ("{start}" BETWEEN re.StartDate AND re.EndDate))) as c \
                FROM `HOTELS` h CROSS JOIN `ROOMS` r HAVING c<m ORDER BY hotel, price;'.format(start=start, end=end), (months,),)
            rows = dbcursor.fetchall()
            hotels = {}
            for prod in rows:
                if (prod[0], prod[4]) in hotels:
                    hotels[(prod[0], prod[4])][prod[1]] = [
                        prod[2], prod[3], prod[4]]
                else:
                    hotels[(prod[0], prod[4])] = {
                        prod[1]: [prod[2], prod[3], prod[4]]}
            dbcursor.execute(
                'SELECT h.HotelLocation as hotel, Description, \
                h.NumberOfRooms as m, \
                (SELECT COUNT(*) FROM `RESERVATIONS` re \
                WHERE re.Cancelled=false AND h.HotelLocation=re.HotelLocation AND \
                ((re.StartDate BETWEEN "{start}" AND "{end}") OR ("{start}" BETWEEN re.StartDate AND re.EndDate))) as c \
                FROM `HOTELS` h HAVING c>=m ORDER BY hotel;'.format(start=start, end=end),)
            rows = dbcursor.fetchall()
            dbcursor.close()
            conn.close()  # Connection must be closed
            for hotel in rows[::-1]:
                if (hotel[0], hotel[1]) in hotels:
                    rows.remove(hotel)
            return render_template("home_page.html", hotels=hotels, loggedin="logged_in" in session, currencies=currencies, admin="logged_in" in session and "@hhotels.co.uk" in session["email"], currentCurrency=session["currency"], fullybooked=rows, intervals=intervals, fromdate=start, todate=end,)
    return render_template("base.html", error="There was an error connecting to database",)


@app.route("/booking", methods=["GET", "POST"])
def bookings():
    if "rid" in session:
        os.remove(os.path.join(app.root_path, "receipts",
                  "booking%s.txt" % session["rid"]))
        session.pop("rid")
    conn = dbfunc.getConnection()  # connection to DB
    if conn != None:  # Checking if connection is None
        if conn.is_connected():
            dbcursor = conn.cursor()  # Creating cursor object
            if not len(currencies):
                get_cur()
            if request.method == "POST":
                today = request.form["today"]
                if "currency" not in session:
                    get_cur()
                    session["currency"] = "GBP"
                hotel = request.form["hotel"]
                roomType = request.form["type"]
                startDate = request.form["from"]
                endDate = request.form["to"]
                people = request.form["people"]
                period = int((datetime.strptime(endDate, "%Y-%m-%d") -
                              datetime.strptime(startDate, "%Y-%m-%d")).days)
                discountDays = int((datetime.strptime(
                    startDate, "%Y-%m-%d") - datetime.strptime(today, "%Y-%m-%d")).days)
                dbcursor.execute(
                    "SELECT IF(%s BETWEEN 4 AND 9, PricePeak, PriceOffPeak) FROM HOTELS WHERE HotelLocation = %s;", (datetime.strptime(startDate, "%Y-%m-%d").month, hotel,),)
                hotelPrice = dbcursor.fetchone()[0]
                dbcursor.execute(
                    "SELECT PricePercentage, ExtraPriceForGuest FROM ROOMS WHERE RoomType = %s;", (roomType,),)
                typePrice = dbcursor.fetchone()
                price = period * \
                    (int(hotelPrice) * (1 +
                                        float(typePrice[0]) + (float(typePrice[1]) * (int(people) - 1))))
                dbcursor.execute(
                    "SELECT UserFName, UserLName FROM USERS WHERE UserEmail = %s;", (session["email"],),)
                user = dbcursor.fetchone()
                dbcursor.execute(
                    "SELECT Discount FROM DISCOUNTS WHERE %s BETWEEN LowerBound AND UpperBound;", (discountDays,),)
                discount = dbcursor.fetchone()
                dbcursor.close()
                conn.close()  # Connection must be closed
                return render_template("booking_page.html", user=user, hotel=hotel, type=roomType, admin="logged_in" in session and "@hhotels.co.uk" in session["email"], today=today, frm=startDate, to=endDate, people=people, period=period, price=price, discount=discount[0], discountDays=discountDays, loggedin="logged_in" in session, currencies=currencies, currentCurrency=session["currency"],)
            return redirect(url_for("index",))
    return render_template("base.html", error="There was an error connecting to database",)


@app.route("/register/", methods=["GET", "POST"])
def register():
    if "rid" in session:
        os.remove(os.path.join(app.root_path, "receipts",
                  "booking%s.txt" % session["rid"]))
        session.pop("rid")
    conn = dbfunc.getConnection()
    if conn != None:  # Checking if connection is None
        if conn.is_connected():
            dbcursor = conn.cursor()  # Creating cursor object
            if not len(currencies):
                get_cur()
            if "currency" not in session:
                get_cur()
                session["currency"] = "GBP"
            dbcursor.execute("SELECT HotelLocation FROM HOTELS;")
            hotelpics = dbcursor.fetchall()
            if "logged_in" in session:
                return redirect(url_for("account",))
            elif request.method == "POST":
                email = request.form["email"]
                password = request.form["password"]
                fname = request.form["fname"]
                lname = request.form["lname"]
                phone = request.form["phone"]
                address = request.form["address"]
                # here we should check if username / email already exists
                password = sha256_crypt.hash((str(password)))
                dbcursor.execute(
                    "SELECT * FROM USERS WHERE UserEmail = %s;", (email,))
                x = dbcursor.fetchone()
                if dbcursor.rowcount > 0:  # this means there is a user with same name
                    return render_template("register_page.html", loggedin="logged_in" in session, currencies=currencies, currentCurrency=session["currency"], admin="logged_in" in session and "@hhotels.co.uk" in session["email"], error="User already exists", hotels=hotelpics,)
                else:  # this means we can add new user
                    dbcursor.execute("INSERT INTO USERS VALUES (%s, %s, %s, %s, %s, %s)",
                                     (email, password, fname, lname, address, phone,),)
                    conn.commit()  # saves data in database
                    dbcursor.close()
                    conn.close()
                    return render_template("register_page.html", loggedin="logged_in" in session, currencies=currencies, currentCurrency=session["currency"], admin="logged_in" in session and "@hhotels.co.uk" in session["email"], hotels=hotelpics, message="Registration was successful, please log in with your new account",)
            else:
                return render_template("register_page.html", loggedin="logged_in" in session, currencies=currencies, currentCurrency=session["currency"], admin="logged_in" in session and "@hhotels.co.uk" in session["email"], hotels=hotelpics,)
    return render_template("base.html", error="There was an error connecting to database",)


@app.route("/account", methods=["GET", "POST"])
def account():
    if "rid" in session:
        os.remove(os.path.join(app.root_path, "receipts",
                  "booking%s.txt" % session["rid"]))
        session.pop("rid")
    conn = dbfunc.getConnection()  # connection to DB
    if conn != None:  # Checking if connection is None
        if conn.is_connected():
            dbcursor = conn.cursor()  # Creating cursor object
            if not len(currencies):
                get_cur()
            if "currency" not in session:
                get_cur()
                session["currency"] = "GBP"
            message = ""
            error = ""
            if request.method == "POST":
                if request.form["formType"] == "loginForm":
                    email = request.form["email"]
                    password = request.form["password"]
                    dbcursor.execute(
                        "SELECT PasswordHash FROM USERS WHERE UserEmail = %s;", (email,))
                    data = dbcursor.fetchone()
                    if dbcursor.rowcount < 1:
                        dbcursor.execute("SELECT HotelLocation FROM HOTELS;")
                        hotelpics = dbcursor.fetchall()
                        return render_template("register_page.html", error="User does not exist", loggedin="logged_in" in session, currencies=currencies, admin="logged_in" in session and "@hhotels.co.uk" in session["email"], currentCurrency=session["currency"], hotels=hotelpics,)
                    else:
                        # data = dbcursor.fetchone()[0] #extracting password
                        # verify passowrd hash and password received from user
                        if sha256_crypt.verify(password, str(data[0])):
                            # set session variables
                            session["logged_in"] = True
                            session["email"] = email
                            message = "Log in was successful"
                        else:
                            dbcursor.execute(
                                "SELECT HotelLocation FROM HOTELS;")
                            hotelpics = dbcursor.fetchall()
                            return render_template("register_page.html", error="Incorrect password", loggedin="logged_in" in session, currencies=currencies, admin="logged_in" in session and "@hhotels.co.uk" in session["email"], currentCurrency=session["currency"], hotels=hotelpics,)
                elif request.form["formType"] == "bookingForm":
                    name = request.form["name"]
                    hotel = request.form["hotel"]
                    roomType = request.form["type"]
                    today = request.form["today"]
                    startDate = request.form["from"]
                    endDate = request.form["to"]
                    period = request.form["period"]
                    people = request.form["people"]
                    price = request.form["price"]
                    dbcursor.execute("INSERT INTO RESERVATIONS (UserEmail, HotelLocation, RoomType, StartDate, EndDate, TotalPrice, Currency, NumberOfPeople, DateOfBooking, Cancelled ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, false);", (
                        session["email"], hotel, roomType, startDate, endDate, price, session["currency"], people, today,),)
                    conn.commit()
                    dbcursor.execute(
                        "SELECT MAX(reservationId) FROM RESERVATIONS;")
                    rid = dbcursor.fetchone()[0]
                    rpath = os.path.join(
                        app.root_path, "receipts", "booking%s.txt" % rid)
                    receipt = open(rpath, "w")
                    receipt.writelines("HORIZON HOTELS\n\n*Booking Info*")
                    receipt.writelines("\n\tBooking ID: %s\n\tName: %s\n\tHotel: %s\n\tType: %s\n\tFrom: %s\n\tTo: %s\n\tNumber of nights: %s\n\tNumber of people: %s\n" %
                                       (rid, name, hotel, roomType, startDate, endDate, period, people))
                    receipt.writelines("\n*Payment Info*")
                    receipt.writelines("\n\tPrice paid: %s\n\tDate of payment: %s\n\tPayment with card ending with: %s\n\tCurrency paid with: %s\n" %
                                       (price, today, request.form["cardnum"][-4:], session["currency"]))
                    receipt.close()
                    session["rid"] = rid
                    message = "Booking was successful"
                    error = "<a href='/download_receipt/%s'><button>download receipt</button></a>" % rid
                elif request.form["formType"] in ["changePassword", "adminchangePassword"]:
                    currentPassword = request.form["currentpassword"]
                    newPassword = request.form["password"]
                    dbcursor.execute(
                        "SELECT PasswordHash FROM USERS WHERE UserEmail = %s;", (session["email"],),)
                    data = dbcursor.fetchone()
                    if sha256_crypt.verify(currentPassword, str(data[0])):
                        if "admin" not in request.form["formType"]:
                            email = session["email"]
                        else:
                            email = request.form["email"]
                        newPassword = sha256_crypt.hash((str(newPassword)))
                        dbcursor.execute(
                            "UPDATE USERS SET PasswordHash = %s WHERE UserEmail = %s;", (newPassword, email,),)
                        conn.commit()
                        message = "Password change was successful"
                    else:
                        error = "Password change was NOT successful, incorrect password"
                elif request.form["formType"] == "updateInfo":
                    email = request.form["email"]
                    password = request.form["currentpassword"]
                    fname = request.form["fname"]
                    lname = request.form["lname"]
                    phone = request.form["phone"]
                    address = request.form["address"]
                    dbcursor.execute(
                        "SELECT PasswordHash FROM USERS WHERE UserEmail = %s;", (session["email"],),)
                    data = dbcursor.fetchone()
                    if sha256_crypt.verify(password, str(data[0])):
                        if email != session["email"]:
                            dbcursor.execute(
                                "SELECT * FROM USERS WHERE UserEmail=%s", (email,))
                            x = dbcursor.fetchone()
                            if dbcursor.rowcount > 0:
                                error = "Updating info was NOT successful, a user already exists with this email"
                        dbcursor.execute("UPDATE USERS SET UserEmail = %s, UserFName = %s, UserLName = %s, UserPhone = %s, UserAddress = %s WHERE UserEmail = %s;", (
                            email, fname, lname, phone, address, session["email"],),)
                        conn.commit()
                        message = "Updating info was successful"
                        session["email"] = email
                    else:
                        error = "Updating info was NOT successful, incorrect password"
                elif request.form["formType"] == "cancelForm":
                    if "@hhotels.co.uk" in session["email"]:
                        dbcursor.execute(
                            "SELECT PasswordHash FROM USERS WHERE UserEmail = %s;", (session["email"],),)
                        data = dbcursor.fetchone()
                        if not sha256_crypt.verify(request.form["currentpassword"], str(data[0])):
                            error = "Booking cancellation was NOT successful, incorrect password"
                        else:
                            dbcursor.execute(
                                "UPDATE RESERVATIONS SET Cancelled=true WHERE ReservationId=%s AND UserEmail=%s;", (request.form["resid"], request.form["email"],),)
                            conn.commit()
                            message = "Booking cancellation was successful"
                    else:
                        dbcursor.execute(
                            "UPDATE RESERVATIONS SET Cancelled=true WHERE ReservationId=%s;", (request.form["resid"],),)
                        conn.commit()
                        message = "Booking cancellation was successful"
                elif request.form["formType"] in ["deleteaccount", "admindeleteaccount"]:
                    dbcursor.execute(
                        "SELECT PasswordHash FROM USERS WHERE UserEmail = %s;", (session["email"],),)
                    data = dbcursor.fetchone()
                    if sha256_crypt.verify(request.form["password"], str(data[0])):
                        if "admin" not in request.form["formType"]:
                            email = session["email"]
                        else:
                            email = request.form["email"]
                        if "admin" in request.form["formType"] and email == session["email"]:
                            error = "Account deletion was NOT successful, have to delete account from delete account"
                        else:
                            dbcursor.execute(
                                "SELECT COUNT(*) FROM RESERVATIONS WHERE UserEmail=%s AND StartDate>%s AND Cancelled=false", (email, date.today(),),)
                            if dbcursor.fetchone()[0]:
                                error = "Account deletion was NOT successful, you need to cancel all bookings first"
                            else:
                                dbcursor.execute(
                                    "DELETE FROM USERS WHERE UserEmail=%s;", (email,),)
                                conn.commit()
                                if "admin" not in request.form["formType"]:
                                    return redirect(url_for("logout",))
                                message = "Account deletion was successful"
                    else:
                        error = "Account deletion was NOT successful, incorrect password"
                elif request.form["formType"] == "newHotel":
                    name = request.form["newHotelName"]
                    pic = request.files["newHotelPic"]
                    rooms = request.form["newHotelRooms"]
                    peak = request.form["newHotelPeak"]
                    offpeak = request.form["newHotelOffPeak"]
                    description = request.form["description"]
                    dbcursor.execute(
                        "SELECT * FROM HOTELS WHERE HotelLocation = %s;", (name,))
                    data = dbcursor.fetchone()
                    if dbcursor.rowcount > 1:  # this mean no user exists
                        error = "Adding a new hotel was NOT successful, hotel already exist"
                    else:
                        pic.save(os.path.join(app.root_path,
                                              "static", "rooms pics", "%s.jpg" % name))
                        dbcursor.execute("INSERT INTO HOTELS VALUES (%s, %s, %s, %s, %s);",
                                         (name, rooms, peak, offpeak, description,),)
                        conn.commit()
                        message = "Adding a new hotel was successful"
                elif request.form["formType"] == "delhotel":
                    hotelid = request.form["hotelid"]
                    dbcursor.execute(
                        "SELECT PasswordHash FROM USERS WHERE UserEmail = %s;", (session["email"],),)
                    data = dbcursor.fetchone()
                    if sha256_crypt.verify(request.form["password"], str(data[0])):
                        dbcursor.execute(
                            "DELETE FROM HOTELS WHERE HotelLocation=%s;", (hotelid,),)
                        conn.commit()
                        try:
                            os.remove(os.path.join(app.root_path,
                                                   "static", "rooms pics", "%s.jpg" % hotelid))
                        except:
                            error = "Deleting picture was unsuccessful"
                        message = "Deleting a hotel was successful"
                    else:
                        error = "Deleting a hotel was NOT successful, incorrect password"
                elif request.form["formType"] == "addcur":
                    curid = request.form["curid"]
                    curval = request.form["curval"]
                    if curid not in currencies:
                        dbcursor.execute(
                            "INSERT INTO CURRENCY_CONV VALUES (%s,%s/100);", (curid, curval,),)
                        conn.commit()
                        get_cur()
                        message = "Adding a new currency was successful"
                    else:
                        error = "Adding a new currency was NOT successf, currency already exists"
                elif request.form["formType"] == "updateHotel":
                    hotel = request.form["hotel"]
                    hotelLocation = request.form["HotelLocation"]
                    pricePeak = request.form["PricePeak"]
                    priceOffPeak = request.form["PriceOffPeak"]
                    description = request.form["Description"]
                    dbcursor.execute(
                        "UPDATE HOTELS SET HotelLocation = %s, PricePeak = %s, PriceOffPeak = %s, Description = %s WHERE HotelLocation = %s;", (hotelLocation, pricePeak, priceOffPeak, description, hotel,),)
                    conn.commit()
                    try:

                        os.rename(os.path.join(app.root_path,
                                               "static", "rooms pics", "%s.jpg" % hotel),
                                  os.path.join(app.root_path,
                                               "static", "rooms pics", "%s.jpg" % hotelLocation))
                    except:
                        error = "Updating picture name was unsuccessful"
                    message = "Updating hotel data was successful"
            if "logged_in" not in session:
                return redirect(url_for("register",))
            hotels = {}
            hoteltodel = []
            stats = []
            userdata = []
            resdata = []
            dbcursor.execute(
                "SELECT * FROM USERS WHERE UserEmail=%s", (session["email"],),)
            userdata = dbcursor.fetchone()
            if "@hhotels.co.uk" not in session["email"]:
                dbcursor.execute(
                    "SELECT rs.*,DATEDIFF(rs.StartDate, %s) as days, \
                    (SELECT rf.Refund FROM REFUNDS rf WHERE days BETWEEN rf.LowerBound AND rf.UpperBound) \
                    FROM RESERVATIONS rs WHERE UserEmail=%s", (date.today(), session["email"],),)
                resdata = dbcursor.fetchall()
            else:
                dbcursor.execute("SELECT * FROM HOTELS;")
                hoteld = dbcursor.fetchall()
                for hotel in hoteld:
                    hotels[hotel[0]] = [hotel[0], hotel[2], hotel[3], hotel[4]]
                dbcursor.execute(
                    "SELECT h.HotelLocation FROM `HOTELS` h WHERE \
                    (SELECT COUNT(r.HotelLocation) FROM `RESERVATIONS` r \
                        WHERE h.HotelLocation=r.HotelLocation  AND r.EndDate>%s AND r.Cancelled=false)=0;", (date.today(),),)
                hoteltodel = dbcursor.fetchall()
                dbcursor.execute('SELECT h.hotelLocation, (SELECT COUNT(*) FROM `RESERVATIONS` r WHERE h.HotelLocation=r.HotelLocation AND Cancelled=false AND StartDate BETWEEN "{sdate}" AND "{ndate}") as res,\
                                    IFNULL((SELECT SUM(ROUND(TotalPrice/(SELECT ChangeRate FROM `CURRENCY_CONV` WHERE Currency=r.Currency))) FROM `RESERVATIONS` r WHERE h.HotelLocation=r.HotelLocation AND Cancelled=false AND DateOfBooking BETWEEN "{sdate}" AND "{ndate}"), 0) as rev,\
                                    (SELECT COUNT(*) FROM `RESERVATIONS` r WHERE h.HotelLocation=r.HotelLocation AND Cancelled=true AND StartDate BETWEEN "{sdate}" AND "{ndate}") as can FROM `HOTELS` h ORDER BY res DESC, rev DESC, can ASC, HotelLocation\
                                    '.format(sdate=date.today() + timedelta(days=-30), ndate=date.today()))
                stats = dbcursor.fetchall()
            dbcursor.close()
            conn.close()  # Connection must be closed
            return render_template("account_page.html", message=message, error=error, stats=stats, hotels=hotels, hoteltodel=hoteltodel, userdata=userdata, resdata=resdata, today=date.today(), admin="logged_in" in session and "@hhotels.co.uk" in session["email"], loggedin="logged_in" in session, currencies=currencies, currentCurrency=session["currency"],)
    return render_template("base.html", error="There was an error connecting to database",)


@ app.route("/logout/")
def logout():
    if "rid" in session:
        os.remove(os.path.join(app.root_path, "receipts",
                  "booking%s.txt" % session["rid"]))
        session.pop("rid")
    if "logged_in" in session:
        crncy = session["currency"]
        session.clear()
        session["currency"] = crncy
        return redirect(request.referrer)
    return redirect(url_for("index",))


@ app.route("/policies")
def policies():
    if "rid" in session:
        os.remove(os.path.join(app.root_path, "receipts",
                  "booking%s.txt" % session["rid"]))
        session.pop("rid")
    conn = dbfunc.getConnection()  # connection to DB3
    if conn != None:  # Checking if connection is None
        if conn.is_connected():
            dbcursor = conn.cursor()  # Creating cursor object
            if not len(currencies):
                get_cur()
            if "currency" not in session:
                get_cur()
                session["currency"] = "GBP"
            dbcursor.execute("SELECT * FROM DISCOUNTS ORDER BY Discount DESC;")
            discounts = dbcursor.fetchall()
            dbcursor.execute("SELECT * FROM REFUNDS ORDER BY refund DESC;")
            refunds = dbcursor.fetchall()
            dbcursor.execute(
                "SELECT RoomType, FLOOR(PricePercentage*100), MaxCapacity, FLOOR(ExtraPriceForGuest*100) FROM ROOMS ORDER BY MaxCapacity ASC;")
            rooms = dbcursor.fetchall()
            dbcursor.close()
            conn.close()  # Connection must be closed
            return render_template("policies_page.html", loggedin="logged_in" in session, currencies=currencies, currentCurrency=session["currency"], admin="logged_in" in session and "@hhotels.co.uk" in session["email"], discounts=discounts, refunds=refunds, rooms=rooms,)
    return render_template("base.html", error="There was an error connecting to database",)


@ app.route('/download_receipt/<rid>')
def download(rid):
    return send_file(os.path.join(app.root_path, "receipts", "booking%s.txt" % rid), as_attachment=True)


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('base.html', error="Page was not found"), 404


app.run(debug=True)
