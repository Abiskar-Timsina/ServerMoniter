import smtplib
from email.message import EmailMessage

#importing class from classes dir
from classes.diskspace import Disk


def main():
	msg = EmailMessage()
	msg['Subject'] = 'Server Status'
	msg['From'] = #<Your Email Address>
	msg['To'] = #<Target Email Address>

	obj = Disk()
	obj.main_run()
	data = obj.drive_info


	drive = data['drive']
	total=data['total']
	used=data['used']

	message = f'Disk Usuage of the Server Drive : {drive}\nTotal: {total}GB\nUsed:{used}GB'
	with open('Graph1.png','rb') as f:
		data = f.read()

	with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
		smtp.login('<Your Email Address>', Disk().password)

		msg.set_content(message)
		msg.add_attachment(data,maintype='image',subtype='png',filename='graph')
		
		smtp.send_message(msg)

if __name__ == '__main__':
	main()