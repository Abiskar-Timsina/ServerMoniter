import smtplib
import os
from email.message import EmailMessage

from classes.diskspace import Disk
from classes.credentials import Credentials


def main():
    if (Credentials().check()):
        moniter()
    else:
        Credentials().credential_config()


def moniter():
    msg = EmailMessage()
    msg['Subject'] = Credentials().credentails['subject']
    msg['From'] = Credentials().credentails['email']
    msg['To'] = Credentials().credentails['target_email']
    password = Credentials().credentails['password']

    # creating an object for Disk class
    disk_object = Disk()
    disk_object.main_run()
    disk_info = disk_object.drive_info

    # retriving relavent info
    drive, total, used, available, percent_used = disk_info['drive'], disk_info[
        'total'], disk_info['used'], disk_info['available'], disk_info['percent_used'],

    # formatting the type of message to be sent
    message = f'Disk Usuage Summary\nDrive : {drive}\nTotal: {total} GB\nUsed: {used} GB\nAvailable: {available} GB\nUsed Disk: {percent_used}%'

    # opening the the graph
    path = os.getcwd()
    with open(os.path.join(path, 'classes/Config/Graph.png'), 'rb') as f:
        data = f.read()

    # sending the email

    # 465 is the general smtp port
    # smtp.gmail.com is the service for gmail

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        # email as defined earlier, .password is an attribute of the Disk class
        # that just stores the password
        smtp.login(msg['From'], password)

        # set the body of the message
        msg.set_content(message)

        # adding the image of the graph as attachment
        msg.add_attachment(data, maintype='image',
                           subtype='png', filename='graph')

        # sending the final message
        smtp.send_message(msg)

    os.remove(os.path.join(path, 'classes/Config/Graph.png'))

if __name__ == '__main__':
    main()
