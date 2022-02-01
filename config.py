#Bot settings
TOKEN = ""
YOUTOKEN = ""
SBERTOKEN = ""
reciption_mail = ""
reciption_id = 0000000000
m_user_mail = ""
admin_id = 1097478693
current_write = "0"

#Finite State Machine
registration = False
is_mailing = False

#Functions
def isFile(filename):
	try:
		f = open(filename, "r")
		f.close()
		return True
	except:
		return False
