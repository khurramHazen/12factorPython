import bcrypt

'''
You'll need a storage structure to store user related info e.g. usernames & passwords
Right now you'll implement it as Python dictionaries
'''

class UsersDB(object):
	def __init__(self):
		self.DB = {}
		self.DB['user_1'] = { 'username': "Anwar", 'password': 'password', 'password_hash': "$2a$10$KgFhp4HAaBCRAYbFp5XYUOKrbO90yrpUQte4eyafk4Tu6mnZcNWiK", 'email': "anwar@example_mail.com" }
		self.DB['user_2'] = { 'username': "Maqsood",  'password': 'password', 'password_hash': "$2a$10$KgFhp4HAaBCRAYbFp5XYUOKrbO90yrpUQte4eyafk4Tu6mnZcNWiK", 'email': "maqsood@example_mail.com" }

	def match_credentials(self, in_username, in_password):

		if in_username is None or in_password is None:
			return False

		if not in_username in self.DB:
			return False
		
		if not bcrypt.checkpw( in_password, self.DB[in_username]['password_hash'].encode('utf-8') ):
			return False
		
		return True

Users = UsersDB()