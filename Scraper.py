import requests
import re
import requests
import os
import camelot
import time
import mysql.connector
import smtplib
import os
from dotenv import load_dotenv
from email.message import EmailMessage
from bs4 import BeautifulSoup
from datetime import datetime
from pdfrw import PdfReader
from cs50 import SQL
import pandas as pd
from sqlalchemy import create_engine


load_dotenv()

def create_db(file, name):
	disk_engine = create_engine('sqlite:///' + name + ".db")
	tables = camelot.read_pdf(file, pages="all")
	df = pd.concat([tab.df for tab in tables], ignore_index=True)
	df.to_sql('table', con=disk_engine)


files_db = SQL("sqlite:///files.db")


dir_path = dir_path = os.path.dirname(os.path.realpath(__file__)) + "\Files"

res = []

for path in os.listdir(dir_path):
	if os.path.isfile(os.path.join(dir_path, path)):
		if not files_db.execute('SELECT * FROM "links" WHERE "name" = ?', path):
			create_db("Files/"+path, path[:-4])
			date = datetime.now().strftime("%d/%m/%y %H:%M:%S")
			files_db.execute("INSERT INTO links (name, date) VALUES(?, ?)", path, date)


def get_time(feed, file="21-08-2022.db"):
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
		ans += "<p>"+i+"</p>"
	return ans



def send_mail(usremail, feed):
	tmsg=get_time(feed)
	email = os.getenv('gmail')
	password = os.getenv('gmail_pass')

	msg = EmailMessage()
	msg['Subject'] = "Load-shedding Update"
	msg['From'] = email
	msg['To'] = usremail
	msg.set_content(f"Your probable load-shedding time in {feed} for 21-08-2022-Sunday will be at.\n{tmsg}")

	msg.add_alternative(f"""\
	    <!DOCTYPE html>
	        <html>
	            <body>
	                <p>Your probable load-shedding time in {feed} for 21-08-2022-Sunday will be at.<p>
	                <br>
	                {tmsg}

	                <small>Sorry, if multiple emails were sent. I am still testing this on a big database.</>
	            </body>
	        </html>
	    """, subtype='html')


	with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

	    smtp.login(email, password)

	    smtp.send_message(msg)

# mydb = mysql.connector.connect(
#     host="sql6.freemysqlhosting.net",
#     user="sql6513941",
#     password="IpJqEcRWJJ",
#     database="sql6513941")

# my_cursor = mydb.cursor()

# my_cursor.execute("SELECT email, feed FROM users")
# for db in my_cursor:
# 	print(db)
	# get_time(db[1])
# def scrape():
# 	res = requests.get('http://desco.gov.bd/site/page/bbf5acea-f100-438b-964a-829547c45002/-').text
# 	soup = BeautifulSoup(res, 'lxml')
# 	contents = soup.find_all('a')
# 	urls = []

# 	for content in contents:
# 		i = content.get('href')

# 		if i[-3:]=="pdf":
# 			if re.findall("^//desco.portal.gov.bd/uploader/server/../../sites/default/files/files/desco.portal.gov.bd/page/659bb373_82c2_4282_a4f1_cdafbefe0378", i):
# 				file = requests.get("http:"+i, stream=True)
# 				newName = PdfReader(file.raw).Info.Title[4:]
# 				for j in range(len(newName)):
# 					if newName[j].isnumeric():
# 						newName = newName[j:-5]
# 						break
# 				print("http:"+i)
# 				if not files_db.execute('SELECT * FROM "	links" WHERE "name" = ?', newName):
# 					urllib.request.urlretrieve("http:"+i, "00000001.pdf")
# 					# create_db(newName+".pdf", newName)
# 					# date = datetime.now().strftime("%d/%m/%y %H:%M:%S")
# 					# files_db.execute("INSERT INTO links (name, date) VALUES(?, ?)", newName, date)