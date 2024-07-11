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
    print("Enter destination")
    destination =input()
                
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
            print("1.Want to calculate average Account Balance of all users.\n")
            print("2.Want to count the number of rides done by user with specified UserID.\n")
            print("3.Want to count the number of rides done by driver with specified DriverID.\n")
            print("4.Want to see {1-> users , 2-> drivers , 3-> rides , 4-> cabs}\n")
            print("5.Logout\n")
            n4=int(input())
            if(n4==1):
                mycursor=mydb.cursor()
                sql  = "SELECT avg(accountbalance) FROM user WHERE UserID >0;"
                mycursor.execute(sql)
                detail=mycursor.fetchall()
                print(tabulate(detail, headers=[i[0] for i in mycursor.description]))
                mydb.commit()
            if(n4==2):
                mycursor=mydb.cursor()
                UserID = int(input())
                sql = "SELECT count(RideID) FROM ride WHERE UserID = %s;"
                val = (UserID,)
                mycursor.execute(sql,val)
                detail=mycursor.fetchall()
                print(tabulate(detail, headers=[i[0] for i in mycursor.description]))
                mydb.commit()
            if(n4==3):
                mycursor=mydb.cursor()
                DriverID = int(input())
                sql = "SELECT count(RideID) FROM ride WHERE DriverID = %s;"
                val = (DriverID,)
                mycursor.execute(sql,val)
                detail=mycursor.fetchall()
                print(tabulate(detail, headers=[i[0] for i in mycursor.description]))
                mydb.commit()
            if(n4==4):
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
            if(n4==5):
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
                