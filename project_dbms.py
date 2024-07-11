import mysql.connector
import random
import datetime
from tabulate import tabulate

# establish a connection to the MySQL database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="fiitjeesouth",
  database="cabbookingsystem1"
)

admin_id= "Apple"
admin_paasword="saket@45"

def check_login(id,password):
    if(id==admin_id and password ==admin_paasword):
        return True
    return False

# define a function for user login
def login():
    MobileNo = int(input("Enter your MobileNo: "))

    # validate the user credentials in the MySQL database
    mycursor = mydb.cursor()
    sql = "SELECT UserID FROM usermobileno WHERE MobileNo = %s"
    val = (MobileNo,)
    mycursor.execute(sql, val)
    userid = mycursor.fetchone()
    mydb.commit()
    if userid:
        print("Login successful!")
        return userid
    else:
        print("Invalid user, you have to sign up")
        return None

# define a function for user sign up
def signup():
    Firstname = input("Enter your Firstname: ")
    Middlename = input("Enter your Middlename: ")
    Lastname = input("Enter your Lastname: ")
    MobileNo = int(input("Enter your MobileNo: "))
    Location = input("Enter your location: ")
    Money = int(input("Enter the money you want to add: "))

    # validate the user credentials in the MySQL database
    mycursor = mydb.cursor()
    sql = "SELECT MobileNo FROM usermobileno WHERE MobileNo = %s"
    val = (MobileNo,)
    mycursor.execute(sql, val)
    user = mycursor.fetchone()
    mydb.commit()

    if user:
        print("You are already SignUped")
        return
    
    mycursor.execute("SELECT COUNT(*) FROM User")
    result = mycursor.fetchone()
    mydb.commit()

    # insert the user details into the MySQL database
    mycursor = mydb.cursor()
    sql = "insert into User (UserID, Firstname, Middlename, Lastname, AccountBalance, Destination, Location) values (%s,%s,%s,%s,%s,%s,%s);"
    val = (result[0]+1,Firstname,Middlename,Lastname,Money,None,Location,)
    mycursor.execute(sql, val)
    mydb.commit()
    
    sql = "insert into UserMobileNo (UserID, MobileNo) values (%s,%s);"
    val = (result[0]+1,MobileNo,)
    mycursor.execute(sql, val)
    mydb.commit()
    
    print("Sign up successful!")
    

# define a function for booking a cab
def book_cab(userid):
    mycursor=mydb.cursor()
    print("Enter destination")
    destination =input()
    sql= "update user set Destination = %s where UserID = %s;"
    val= (destination,userid,)
    mycursor.execute(sql, val)
    mydb.commit()
                
    print("Cab booking is being requested")
    mycursor=mydb.cursor()
    mycursor.execute("SELECT COUNT(*) FROM Driver")
    result1 = mycursor.fetchone()
    mydb.commit()
    if(result1[0]!=0): 
        print("Driver's side")
        print("Confirm or Cancel the ride!")
        print("1.Confirm")
        print("2.Cancel")
        v=int(input())
        if(v==1):   
            print("Fare you have to pay")
            fare = random.randint(1000, 9999)
            print("Your Fare")
            print(fare)
            print("User's side")
            print("Do you want to go on this fare")
            print("1.Yes")
            print("2.No")
            n1=int(input())
            if(n1==1):
                mycursor=mydb.cursor()
                sql = ("select AccountBalance from user where UserID = %s")
                val =(userid,)
                mycursor.execute(sql,val)
                balance = mycursor.fetchone()
                mydb.commit()
                while(fare>balance[0]):
                    print(f"You don't have sufficient balance! Rs {balance}")
                    print("Do you want to add money?")
                    print("1.Yes")
                    print("2.No")
                    n2=int(input())
                    if(n2==1):
                        print("Enter the amount you want to add")
                        n3=int(input())
                        add_money(n3, userid)
                        sql = ("select AccountBalance from user where UserID = %s")
                        val =(userid,)
                        mycursor=mydb.cursor()
                        mycursor.execute(sql,val)
                        balance = mycursor.fetchone()
                        mydb.commit()
                    if(n2==2):
                        return None
                now = datetime.datetime.now()
                year = now.year
                month = now.month
                day = now.day
                hour = now.hour
                minute = now.minute
                second = now.second
                driverid=random.randint(1,result1[0])
                mycursor.execute("SELECT COUNT(*) FROM Ride")
                result2 = mycursor.fetchone()
                sql= "INSERT INTO Ride (RideID,Fare,Days,Months,Years,Hours,Minutes,Seconds,UserID,DriverID) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
                val= (result2[0]+1,fare,day,month,year,hour,minute,second,userid,driverid,)
                mycursor.execute(sql, val)
                mydb.commit()
                
                print("Your ride completed")
                print("You have to make payment")
                while(True):
                    print("PAY by clicking 1")
                    n=int(input())
                    if(n==1):
                        make_payment(int(useridval[0]),driverid,fare,mydb)
                        return
                    if(n!=1):
                        print("wrong entry")
            if(n1==2):
                print("Fare not accepted, try for another cab")
                return 
        if(v==2):
            print("Driver declines the ride, try for another cab")
            return 
    if(result1[0]==0):
        print("No driver available")
        return 
    return 

# define a function for making a payment
def make_payment(userid,driverid,fare,db):
    mycursor=mydb.cursor()
    sql  = "update user set AccountBalance = AccountBalance - %s where UserID = %s;"
    val = (fare,userid,)
    mycursor.execute(sql,val)
    mydb.commit()
    # deduct the amount from the user
    
    mycursor=mydb.cursor()
    sql  = "update driver set AccountBalance = AccountBalance + %s where DriverID = %s;"
    val = (fare,driverid,)
    mycursor.execute(sql,val)
    mydb.commit()
    
    print("Payment happened successful")
    return 

def view_balance(userid):
    mycursor=mydb.cursor()
    sql  = "select AccountBalance from user where UserID = %s;"
    val = (userid,)
    mycursor.execute(sql,val)
    balance1=mycursor.fetchone()
    mydb.commit()
    print(f"Your Account Balance is {int(balance1[0])}")
    return

def add_money(money,userid):
    mycursor=mydb.cursor()
    sql  = "update user set AccountBalance = AccountBalance + %s where UserID = %s;"
    val = (money,userid,)
    mycursor.execute(sql,val)
    mydb.commit()
    print("Money added successfully")
    return

while(True):
    print("Select Admin or User")
    print("1. Admin")
    print("2. User")
    print("3. Exit")
    n5=int(input())
    if(n5==1):
        adminid = input("Enter login id: ")
        password = input("Enter the password: ")
        check = check_login(admin_id, password)
        if(check==True):
            print("Login Successfull")
        else:
            print("Invalid Admin! Incorrect ID or Password")
        while(check == True):
            print("What you want to do?")
            print("1.Want to know all RideID in which user travel with Driver having driverID greter than 60.\n")
            print("2.Want to count the number of rides of a user whose UserID is equal to 45.\n")
            print("3.Want to calculate average Account Balance of all users.\n")
            print("4.Want to see all details about rides order by UserID in descending and in that DriverID in ascending.\n")
            print("5.Want to see firstname and id of drivers and users whose UserID is same as DriverID.\n")
            print("6.Want to see mobile number of users and of drivers in a column in a table.\n")
            print("7.Want to see firstname of drivers whom account balance is greater than average account balance of all drivers.\n")
            print("8.Want to see firstname of users whom UserID matches with DriverID between 45 and 95.\n")
            print("9.Want to see CabID of Cabs if any driver have account balance between 25000 to 45000.\n")
            print("10.Want to update mobile number of user's whom UserID is minimum between UserID range of 25 to 27.\n")
            print("11.Want to see sum of account balance of driver first order by none then by UserID and finally by both UserID and DriverID.\n")
            print("12.Want to see sum of account balance of user first order by none and then by UserID.\n")
            print("13.Want to see sum of fare of rides firstly order by both UserID and DriverID then only by UserId and finally only by DriverID.\n")
            print("14.Want to see sum of fare of rides order by combination of any two at a time RideID,UserID and DriverID.\n")
            print("15.Want to count the number of rides done by user with UserID = 11.\n")
            print("16.Want to calculate average account balance of user whose UserID is greater than 40.\n")
            print("17.Want to assign class to user according to account balance (>25000 -> vip) and (otherwise -> normal)\n")
            print("18.Want to set fare for ride such that fare will be 1000 for user having UserID>54 and otherwise 2500.\n")
            print("19.Want to see {1-> users , 2-> drivers , 3-> rides , 4-> cabs}\n")
            print("20.Want to delete assign class system or set fare system.")
            print("21.Logout\n")
            n4=int(input())
            if(n4==1):
                mycursor=mydb.cursor()
                sql  = "SELECT RideID FROM ride WHERE UserID IN (SELECT UserID FROM driver WHERE DriverID>60);"
                mycursor.execute(sql)
                detail=mycursor.fetchall()
                print(tabulate(detail, headers=[i[0] for i in mycursor.description]))
                mydb.commit()
            if(n4==2):
                mycursor=mydb.cursor()
                sql  = "SELECT count(RideID) FROM ride WHERE UserID =45;"
                mycursor.execute(sql)
                detail=mycursor.fetchall()
                print(tabulate(detail, headers=[i[0] for i in mycursor.description]))
                mydb.commit()
            if(n4==3):
                mycursor=mydb.cursor()
                sql  = "SELECT avg(accountbalance) FROM user WHERE UserID >0;"
                mycursor.execute(sql)
                detail=mycursor.fetchall()
                print(tabulate(detail, headers=[i[0] for i in mycursor.description]))
                mydb.commit()
            if(n4==4):
                mycursor=mydb.cursor()
                sql  = "select * from ride order by UserID desc, DriverID asc;"
                mycursor.execute(sql)
                detail=mycursor.fetchall()
                print(tabulate(detail, headers=[i[0] for i in mycursor.description]))
                mydb.commit()
            if(n4==5):
                mycursor=mydb.cursor()
                sql  = "SELECT User.UserID, User.Firstname, Driver.DriverID, Driver.Firstname FROM driver INNER JOIN User ON Driver.UserID=User.UserID;"
                mycursor.execute(sql)
                detail=mycursor.fetchall()
                print(tabulate(detail, headers=[i[0] for i in mycursor.description]))
                mydb.commit()
            if(n4==6):
                mycursor=mydb.cursor()
                sql  = "select MobileNo from usermobileno union select MobileNo from drivermobileno;"
                mycursor.execute(sql)
                detail=mycursor.fetchall()
                print(tabulate(detail, headers=[i[0] for i in mycursor.description]))
                mydb.commit()
            if(n4==7):
                mycursor=mydb.cursor()
                sql  = "select Firstname from driver where AccountBalance > (select avg(AccountBalance) from driver);"
                mycursor.execute(sql)
                detail=mycursor.fetchall()
                print(tabulate(detail, headers=[i[0] for i in mycursor.description]))
                mydb.commit()
            if(n4==8):
                mycursor=mydb.cursor()
                sql  = "SELECT Firstname FROM user where UserID between (select DriverID from driver where DriverID =45) and (select DriverID from driver where DriverID =95);"
                mycursor.execute(sql)
                detail=mycursor.fetchall()
                print(tabulate(detail, headers=[i[0] for i in mycursor.description]))
                mydb.commit()
            if(n4==9):
                mycursor=mydb.cursor()
                sql  = "SELECT CabID FROM cab WHERE CabID = ANY (SELECT DriverID FROM driver WHERE AccountBalance between 25000 and 45000);"
                mycursor.execute(sql)
                detail=mycursor.fetchall()
                print(tabulate(detail, headers=[i[0] for i in mycursor.description]))
                mydb.commit()
            if(n4==10):
                mycursor=mydb.cursor()
                sql  = """UPDATE usermobileno
                        SET MobileNo = '764975'
                        WHERE UserID =(select min(UserID) from user where UserID between 25 and 27);"""
                mycursor.execute(sql)
                print("Number updated successfully!")
                mydb.commit()
            if(n4==11):
                mycursor=mydb.cursor()
                sql = """SELECT NULL as UserID, NULL as DriverID, sum(AccountBalance)
                        FROM Driver
                        UNION ALL
                        SELECT UserID, NULL as DriverID, sum(AccountBalance)
                        FROM Driver
                        GROUP BY UserID
                        UNION ALL
                        SELECT UserID, DriverID, AccountBalance
                        FROM Driver
                        GROUP BY UserID, DriverID;"""
                mycursor.execute(sql)
                detail=mycursor.fetchall()
                print(tabulate(detail, headers=[i[0] for i in mycursor.description]))
                mydb.commit()
            if(n4==12):
                mycursor=mydb.cursor()
                sql = "SELECT NULL as UserID, sum(AccountBalance) FROM User UNION ALL SELECT UserID, sum(AccountBalance) FROM User GROUP BY UserID;"
                mycursor.execute(sql)
                detail=mycursor.fetchall()
                print(tabulate(detail, headers=[i[0] for i in mycursor.description]))
                mydb.commit()
            if(n4==13):
                mycursor=mydb.cursor()
                sql = """SELECT UserID, DriverID, SUM(fare)
                            FROM Ride
                            GROUP BY UserID,DriverID
                            UNION ALL
                            SELECT NULL as UserID, DriverID, SUM(fare)
                            FROM Ride
                            GROUP BY DriverID
                            UNION ALL
                            SELECT UserID, NULL as DriverID, SUM(fare)
                            FROM Ride
                            GROUP BY UserID;"""
                mycursor.execute(sql)
                detail=mycursor.fetchall()
                print(tabulate(detail, headers=[i[0] for i in mycursor.description]))
                mydb.commit()
            if(n4==14):
                mycursor=mydb.cursor()
                sql = """select UserID,DriverID,RideID,SUM(fare)
                            from Ride
                            group by UserID,DriverID,RideID
                            union all
                            select null,DriverID,RideID,sum(fare)
                            from Ride
                            group by DriverID,RideID
                            union all
                            select UserID,null,RideID,sum(fare)
                            from Ride
                            group by UserID,RideID
                            union all
                            select UserID,DriverID,null,sum(fare)
                            from Ride
                            group by UserID,DriverID
                            union all
                            select null,null,RideID,sum(fare)
                            from Ride
                            group by RideID
                            union all
                            select UserID,null ,null ,sum(fare)
                            from Ride
                            group by UserID
                            union all 
                            select null ,DriverID,null ,sum(fare)
                            from Ride
                            group by DriverID
                            union all
                            select null ,null ,null ,sum(fare)
                            from Ride;
                            """
                mycursor.execute(sql)
                detail=mycursor.fetchall()
                print(tabulate(detail, headers=[i[0] for i in mycursor.description]))
                mydb.commit()
            if(n4==15):
                mycursor=mydb.cursor()
                sql = "SELECT count(RideID) FROM ride WHERE UserID =11;"
                mycursor.execute(sql)
                detail=mycursor.fetchall()
                print(tabulate(detail, headers=[i[0] for i in mycursor.description]))
                mydb.commit()
            if(n4==16):
                mycursor=mydb.cursor()
                sql = "SELECT avg(accountbalance) FROM user WHERE UserID>40;"
                mycursor.execute(sql)
                detail=mycursor.fetchall()
                print(tabulate(detail, headers=[i[0] for i in mycursor.description]))
                mydb.commit()
            if(n4==17):
                mycursor=mydb.cursor()
                mycursor.execute("drop trigger if exists assignclass")
                mycursor.execute("""CREATE TRIGGER assignclass
                before insert
                ON user
                FOR EACH ROW
                BEGIN
                IF NEW.AccountBalance>25000 THEN
                    set NEW.class = 'Vip';
                ELSE 
                    set NEW.class = 'Normal';
                END IF;
                END;
                """)
                print("System created!")
                mydb.commit()
            if(n4==18):
                mycursor=mydb.cursor()
                mycursor.execute("drop trigger if exists setfare")
                mycursor.execute("""CREATE TRIGGER setfare
                before insert
                ON ride
                FOR EACH ROW
                BEGIN
                IF NEW.UserID>54 THEN
                    set NEW.fare = 1000;
                ELSE 
                    set NEW.fare = 2500;
                END IF;
                END;
                """)
                print("System created!")
                mydb.commit()
            if(n4==19):
                n9=int(input())
                if(n9==1):
                    print("1.From UserID    2.Whole Entries")
                    n11=int(input())
                    if(n11==1):
                        print("Enter UserID")
                        n10=int(input())
                        mycursor=mydb.cursor()
                        sql  = "Select * from user where UserID = %s;"
                        val = (n10,)
                        mycursor.execute(sql,val)
                        detail=mycursor.fetchall()
                        print(tabulate(detail, headers=[i[0] for i in mycursor.description]))
                        mydb.commit()
                    if(n11==2):
                        sql  = "Select * from user;"
                        mycursor.execute(sql)
                        detail=mycursor.fetchall()
                        print(tabulate(detail, headers=[i[0] for i in mycursor.description]))
                        mydb.commit()
                if(n9==2):
                    print("1.From DriverID    2.Whole Entries")
                    n12=int(input())
                    if(n12==1):
                        print("Enter DriverID")
                        n10=int(input())
                        mycursor=mydb.cursor()
                        sql  = "Select * from driver where DriverID = %s;"
                        val = (n10,)
                        mycursor.execute(sql,val)
                        detail=mycursor.fetchall()
                        print(tabulate(detail, headers=[i[0] for i in mycursor.description]))
                        mydb.commit()
                    if(n12==2):
                        sql  = "Select * from driver;"
                        mycursor.execute(sql)
                        detail=mycursor.fetchall()
                        print(tabulate(detail, headers=[i[0] for i in mycursor.description]))
                        mydb.commit()
                if(n9==3):
                    print("1.From RideID    2.Whole Entries")
                    n13=int(input())
                    if(n13==1):
                        print("Enter RideID")
                        n10=int(input())
                        mycursor=mydb.cursor()
                        sql  = "Select * from ride where RideID = %s;"
                        val = (n10,)
                        mycursor.execute(sql,val)
                        detail=mycursor.fetchall()
                        print(tabulate(detail, headers=[i[0] for i in mycursor.description]))
                        mydb.commit()
                    if(n13==2):
                        sql  = "Select * from ride;"
                        mycursor.execute(sql)
                        detail=mycursor.fetchall()
                        print(tabulate(detail, headers=[i[0] for i in mycursor.description]))
                        mydb.commit()
                if(n9==4):
                    print("1.From CabID    2.Whole Entries")
                    n14=int(input())
                    if(n14==1):
                        print("Enter CabID")
                        n10=int(input())
                        mycursor=mydb.cursor()
                        sql  = "Select * from cab where CabID = %s;"
                        val = (n10,)
                        mycursor.execute(sql,val)
                        detail=mycursor.fetchall()
                        print(tabulate(detail, headers=[i[0] for i in mycursor.description]))
                        mydb.commit()
                    if(n14==2):
                        sql  = "Select * from cab;"
                        mycursor.execute(sql)
                        detail=mycursor.fetchall()
                        print(tabulate(detail, headers=[i[0] for i in mycursor.description]))
                        mydb.commit()
            if(n4==20):
                print("1.Set far    2.Set class")
                n20=int(input())
                if(n20==1):
                    mycursor=mydb.cursor()
                    mycursor.execute("drop trigger if exists setfare")
                    mydb.commit()
                    print("Deleted successfully!")
                if(n20==2):
                    mycursor=mydb.cursor()
                    mycursor.execute("drop trigger if exists assignclass")
                    mydb.commit()
                    print("Deleted successfully!")
            if(n4==21):
                break
    if(n5==2):
        while(True):
            print(""" Welcome to UBELA, your customized cab booking service!\n
        Choose from below whatever you want:\n
        1.Login\n
        2.SignUp\n
        3.Back
        """)
            p=int(input())
            if(p==1):
                useridval=login()
                if(useridval!=None):
                    while(True):
                        print("""Now you can choose from below menu:
                        1. Book a Cab
                        2. View AccountBalance
                        3. Add Money
                        4. Logout""")
                        q=int((input()))
                        if(q==1):
                            book_cab(int(useridval[0]))
                        if(q==2):
                            view_balance(int(useridval[0]))
                        if(q==3):
                            print("Enter the money you want to add ->")
                            money=int(input())
                            add_money(money,int(useridval[0]))
                        if(q==4):
                            break
            if(p==2):
                signup()
            if(p==3):
                break
    if(n5==3):
        mydb.commit()
        print("Application exited successfully!")
        break
                