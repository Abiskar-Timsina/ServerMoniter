import smtplib
from email.message import EmailMessage

#importing class from classes dir
from classes.diskspace import Disk


def main():
	msg = EmailMessage()
	msg['Subject'] = 'Server Status'
	msg['From'] = 'abiskartimsina4mini@gmail.com'
	msg['To'] = 'abiskartimsina4@gmail.com'
	email = msg['From']

	#creating an object for Disk class
	disk_object = Disk()
	disk_object.main_run()
	disk_info = obj.drive_info

	#retriving relavent info 
	drive,total,used = disk_info['drive'],disk_info['total'],disk_info['used']

	#formatting the type of message to be sent
	message = f'Disk Usuage of the Server Drive : {drive}\nTotal: {total}GB\nUsed:{used}GB'
	
	#opening the the graph
	with open('Graph.png','rb') as f:
		data = f.read()

	#sending the email

	#465 is the general smtp port
	#smtp.gmail.com is the service for gmail

	with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
		# email as defined earlier, .password is an attribute of the Disk class that just stores the password 
		smtp.login(email, Disk().password)

		#set the body of the message
		msg.set_content(message)

		#adding the image of the graph as attachment
		msg.add_attachment(data,maintype='image',subtype='png',filename='graph')
		
		#sending the final message
		smtp.send_message(msg)

if __name__ == '__main__':
	main()