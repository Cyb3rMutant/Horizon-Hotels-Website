# purpose:  get connection to database and the commented code is to fully book hotels
# module: Web Development and Databases
# author: Yazeed Abu-Hummos
# UWE ID: 21014295
# last edit time and date: 18:51 04/05/2022


import mysql.connector


def getConnection():
    try:
        conn = mysql.connector.connect(host="localhost",
                                       user="root",
                                       password="password",
                                       database="DBname")
    except mysql.connector.Error as err:
        return None
    else:  # will execute if there is no exception raised in try block
        return conn


# conn = getConnection()
# dbcursor = conn.cursor()
# dbcursor.execute(
#     "SELECT HotelLocation, NumberOfRooms FROM HOTELS WHERE HotelLocation='Glasgow';")
# hotels = dbcursor.fetchall()
# dbcursor.execute("SELECT RoomType, PercentageOfRooms FROM ROOMS;")
# rooms = dbcursor.fetchall()

# for hotel in hotels:
#     for room in rooms:
#         for i in range(int(hotel[1]*room[1])):
#             dbcursor.execute("INSERT INTO `RESERVATIONS`\
#                 (UserEmail,HotelLocation,RoomType,StartDate,EndDate,TotalPrice,NumberOfPeople, Currency, DateOfBooking, Cancelled)\
#                     VALUES ('user@gmail.com', %s, %s, '2022-04-26','2022-05-10',1800,6, 'GBP', '2022-04-24', false);", (hotel[0], room[0],))
#             conn.commit()
