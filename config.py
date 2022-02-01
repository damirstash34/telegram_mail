#Bot settings
TOKEN = "5188353793:AAFETk41gZnnBNHH2CPIzKX2dR4wj7nK4-U"
YOUTOKEN = "381764678:TEST:33035"
SBERTOKEN = "401643678:TEST:cf058708-b3f1-4132-beff-e79e4384331f"
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