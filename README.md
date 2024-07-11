I have made a python cli interface for my cab booking application.
from start it ask from which side  you want to enter admin or user or you want to exit the aplication.
in admin you have to login with the correct id and password. if you have entered right then you will be  logined and see the menu  from which either you can return or see what you want from option available. if incorrect then return to login page of view as admin user or exit application.
if choosen user, then we see menu  to login or signup or go back, if we tried to login with not signup mobile number, program  will print incorrect login and we have to sign up using  firstname, middlename, lastname, location, money and mobile number.Then we returned back to menu of login and signup where we can signup new use or login.

After, login we see menu which have see account balance, add money to account or book cab or logout, so you can do any, in book a cab, when you click(firstly it will ask you to add destination)then it will ask driver whether to accept it or not(if not accepted you will be return back to the  menu) if accepted then you have to agree on fair for ride if agreed then your cab will be booked or account balance is insufficient then asked to add money or return back to menu by not adding.if cab booked then your ride got completed and ask to pay money and until you don't pay it, it will stuck there.if you pay, you will return back to main menu of add money, book cab,see account balance or logout.

sql python connecting -->
login /signup  user -> database checking for mobilenumber or inserting new user
account balance -> adding, substracting or selecting from database(user, driver) 
book cabe -> making entry in ride and user, also randomly selecting driver to assign to user 
