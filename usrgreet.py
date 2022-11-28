import mysql.connector
import requests
import os
import time
import mysql.connector
import smtplib
from dotenv import load_dotenv
from email.message import EmailMessage
from bs4 import BeautifulSoup
from datetime import datetime
from pdfrw import PdfReader
from cs50 import SQL
load_dotenv()

db = SQL("sqlite:///greeted.db")


def greet(id, name, email, feed, code):
    gmail = os.getenv('gmail')
    passd = os.getenv('gmail_pass')

    msg = EmailMessage()
    msg['Subject'] = "Congratulations!"
    msg['From'] = gmail
    msg['To'] = email
    msg.set_content(f"Thank you {name} for subscribing.\nExpect an email reminder of load-shedding timing in {feed} scheduled at 12AM everyday.\n\nSecret \
        Code: {code}\nUse this code to unsubscribe at anytime. We will delete all your information.")

    msg.add_alternative(f"""\
        <!DOCTYPE html>
            <html>
                <body>
                    <h1 style='color:#198754'>Thank you {name} for subscribing.</h1>
                    <br>
                    <p>Expect an email reminder of load-shedding timing in {feed} scheduled at 12AM everyday.<p>
                    <br>
                    <p>Secret Code: {code}</p>
                    <p>Use this code to unsubscribe at anytime. We will delete all your information.</p>
                    <p>
                </body>
            </html>
        """, subtype='html')
    
    db.execute("INSERT INTO greeted (usrid) VALUES(?)", id)


    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

        smtp.login(gmail, passd)

        smtp.send_message(msg)


def get_time(feed, file="04-09-2022.db"):
    db = SQL("sqlite:///"+file)
    rows = db.execute('SELECT * FROM "table" WHERE "2" LIKE ?', feed+"%")

    table = {'0': 'S&D Division Name', '1': 'Area Under the feeder', '2': 'Feeder Name', '3': 'Time', '4': '00:00 - 01:00', '5': '01:00 - 02:00', '6': '02:00 - 03:00', '7': '03:00 - 04:00', '8': '04:00 - 05:00', '9': '05:00 - 06:00', '10': '06:00 - 07:00', '11': '7:00 - 8:00', '12': '8:00 - 9:00', '13': '9:00 - 10:00', '14': '10:00 - 11:00', '15': '11:00 - 12:00', '16': '12:00 - 13:00', '17': '13:00 - 14:00', '18': '14:00 - 15:00', '19': '15:00 - 16:00', '20': '16:00 - 17:00', '21': '17:00 - 18:00', '22': '18:00 - 19:00', '23': '19:00 - 20:00', '24': '20:00 - 21:00', '25': '21:00 - 22:00', '26': '22:00 - 23:00', '27': '23:00 - 00:00'}

    times = []
    
    for i, j in rows[0].items():
        if j:
            if i.isnumeric():
                if int(i)>3:
                    times.append(table[i])

    ans = ""
    for  i in times:
        ans += "<li><h5>"+i+"</li>"+"</h5>"
    return ans

datee = "04-09-2022"
day = "Sunday"

def send_mail(usremail, feed):
    tmsg=get_time(feed)
    email = os.getenv('gmail')
    password = os.getenv('gmail_pass')

    msg = EmailMessage()
    msg['Subject'] = f"{day} Load-shedding Update"
    msg['From'] = email
    msg['To'] = usremail
    msg.set_content(f"Your probable load-shedding time in {feed} for {datee}-{day} will be at.\n{tmsg}")

    msg.add_alternative(f"""\
        <!DOCTYPE html>
            <html>
                <body>
                    <h4>Your probable load-shedding time in {feed} for {datee}-{day} will be at</h4>
                    <ul style='color:#198754;'>
                        {tmsg}
                    </ul>
                    
                </body>
                <small>Want to stop receiving emails? Unsubscribe <a href=https://karentnai.herokuapp.com/unsubscribe>here</a></small>
            </html>
        """, subtype='html')


    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

        smtp.login(email, password)

        smtp.send_message(msg) 


def runn():
    mydb = mysql.connector.connect(
    host="sql6.freemysqlhosting.net",
    user="sql6513941",
    password="IpJqEcRWJJ",
    database="sql6513941")
    
    my_cursor = mydb.cursor()

    my_cursor.execute("SELECT * FROM users WHERE id")

    for dbs in my_cursor:
        # rows = db.execute("SELECT * FROM greeted WHERE usrid=?", dbs[0])

        send_mail(dbs[2], dbs[3])
        print("Sent:", dbs[2])
        # if not rows:
        #     print(dbs[0], dbs[1], "SENT!")
            # greet(dbs[0], dbs[1], dbs[2], dbs[3], dbs[5])

# ran = 0

# db = SQL("sqlite:///"+"23-08-2022.db")
# rows = db.execute('SELECT "0", "1", "2" FROM "table" WHERE "17" AND "14" IS NOT NULL')

# for i in rows:
#     print(i)

runn()


# while True:
#     runn()
#     time.sleep(180)
#     ran += 1
#     print(ran)

