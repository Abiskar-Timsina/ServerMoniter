import pickle
import random
import os


class Credentials(object):

    def __init__(self):
        pass

    def credential_config(self):
        path = os.path.join(os.getcwd(), './classes/Config')
        print('-------------------------------------------------------')
        print('|            ONE-TIME-CONFIGURATION                   |')
        print('-------------------------------------------------------')

        print(f'\nThe address where the email will be sent')
        target_email = input('Enter Target Email : ')
        print(f'\n')

        print(f'The address where the email will be sent from. MUST BE @gmail.com')
        while True:
            email = input('Enter Your Email : ')
            if (email[-10:] != '@gmail.com'):
                print('[ERROR] Your email MUST be @gmail.com\n')
                pass
            else:
                break

        print(f'\nThe password for your email account. (The password is\'nt completly encrypted. DO NOT share .config files.')
        while True:
            password1 = input('Enter password : ')
            password2 = input('Enter the password again : ')

            if (password1 == password2):
                password = password1
                break
            else:
                print('[ERROR] Passwords don\'t match\n')
                pass

        print('[CONFIGURATION COMPLETE]')
        print('[INFO] The Subject of each mail will be "Server Status" unless changed from the emailconfig.txt file.\n')

        randomdata = str(random.randint(10000, 50000) * random.randint(5, 10))

        with open(os.path.join(path, '.config'), 'wb') as f:
            pickle.dump([[randomdata, target_email, randomdata,
                          email, randomdata, password, randomdata]], f)

        with open(os.path.join(path, 'emailconfig.txt'), 'w') as file:
            file.write('Subject=Server Status')

        input('Enter any key to exit...')
        os.sys.exit()

    @property
    def credentails(self):
        path = os.path.join(os.getcwd(), './classes/Config')

        with open(os.path.join(path, '.config'), 'rb') as f:
            data = pickle.load(f)

        for a, b, c, d, e, f, g in data:
            target_email = b
            email = d
            password = f

        with open(os.path.join(path, 'emailconfig.txt'), 'r') as file:
            line = file.readline()
            line = line.split('=')
            subject = line[1]

        # return (target_email,email,password,subject)
        return {'target_email': target_email, 'email': email, 'password': password, 'subject': subject}
        # return target_email

    def check(self):
        path = os.getcwd()
        print(path)
        if (os.path.exists(os.path.join(path, './classes/Config'))):
            del path
            return True
        else:
            os.mkdir(os.path.join(path, './classes/Config'))
            del path
            self.credential_config()
