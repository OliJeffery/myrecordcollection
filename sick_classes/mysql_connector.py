import mysql.connector
import json

class Database:

	def connect(self):
		with open('../../sick_credentials/mysql_credentials.json') as mysql_credentials:
			json_credentials = json.loads(mysql_credentials.read())
			mydb = mysql.connector.connect(
			  		host=json_credentials['host'],
			  		user=json_credentials['user'],
			  		passwd=json_credentials['passwd'],
			  		database=json_credentials['database']
				)
			return mydb

if __name__ == '__main__':
	database = Database()
	connection = database.connect()
	print(connection.get_rows(connection.cmd_query('SELECT * FROM sick_users WHERE user_id = 666')))
