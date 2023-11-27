username='root'
password='mysqlbysss7'
import MySQLdb
db=MySQLdb.connect("localhost",username,password,"mysql");
c=db.cursor()
db=MySQLdb.connect("localhost",username,password,"yt_db");
c=db.cursor()
def checkLogin(user_id,user_password):
	db=MySQLdb.connect("localhost",username,password,"yt_db");
	c=db.cursor()
	query = "select count(*) from users where email= '%s' and password = '%s'" % (user_id, user_password )
	print(query)
	status= (c.execute(query))
	result=c.fetchall()
	print(status)
	return result[0][0]