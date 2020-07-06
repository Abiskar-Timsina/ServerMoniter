import os
import subprocess
from matplotlib import pyplot as plt
import datetime
import time
import pickle


class Disk(object):
    graph_usuage = []
    graph_day = []
    drive_info = {}
    password = #<Your password for the associated gmail>
    

    # this runs the df -h command on terminal and pipes the output to a temp file
    @classmethod
    def read_sys(cls):
        with open('./DiskUsuage.txt', 'w') as f:
            file_data = subprocess.run('df -h', shell=True, text=True, stdout=f)


    # this appends all the relavent info to the drive_info dictionary which is used to retrive total/used space in the main.py file
    @classmethod        
    def ret_fun(cls,**kwargs):
        for arg,value in kwargs.items():
            cls.drive_info.update({arg:value})


    # this method read the output for the read_sys file where each line corresponds to a drive 
    @classmethod
    def read_data(cls):

        with open('./DiskUsuage.txt', 'r') as f:
            a = f.readlines()

        check = len(a)

        for i in range(check):
            i += 3 # 3 because df -h returns the output for temp folders which in this case is not required (for me)

            drive = a[i][0:9] #0:2 for windows # Parsing throught the string to get only  drive name
 
            total = int(a[i][16:19]) #16:19 for windows #Parsing throught the string to get only the total memory allocated

            used = float(a[i][22:25]) #23:25 for windows #Parsing throught the string to get only the used memory

            day = time.localtime().tm_yday 

            '''
            Year day over month day because at the start of each month the x-axis becomes 0; this causes a hard to read graph

            A possible and simple solution is to make multiple graphs and append them to a single plot to differentiate the different months
            which will probably be added in upcoming versions
            '''

            # appending to graph_day / graph_usuage so that it can reatain info about the current state whenever it is called.
            cls.graph_day.append(day)
            cls.graph_usuage.append((used))
            # print(f'Drive: {drive}, Total Space: {total} GB ,Used Space: {used} GB, Available: {total - used} GB, % Used: {int((lambda : (used/total)*100)())} %')
            cls.ret_fun(drive=drive,total=total,used=used)
            break

    '''
    the info.config file contains a single array in the format of;
    [<day>,<space used>]

    which over the time increases as;

    [[<day>,<space used>],[<day1>,<space used1>],[<day2>,<space used2>],[<day3>,<space used3>]]
    '''

    # this is used to update the array stored in the info.config file so that the space used and day/time are retrived and plotted as necessary
    @classmethod
    def update(cls, ar):
        with open('./info.config', 'wb') as f:
            pickle.dump(ar, f)


    #checks the previous saved data and add it to the graph_day,graph_usuage list to be plotted again
    @classmethod
    def check_prev(cls):
	    if(os.path.exists('./info.config')):
	        with open('./info.config', 'rb') as file:
	            data = pickle.load(file)

	        for d in data[0]:
	            cls.graph_day.append(d)
	        for u in data[1]:
	            cls.graph_usuage.append(u)

    # this method plots the graph using matplotlib 
    @classmethod
    def save_data(cls):
        plt.style.use('dark_background')
        plt.title('Server Disk Usuage: 2020')
        plt.xlabel('Day of the Year')
        plt.ylabel('Space Used')
        plt.plot(cls.graph_day, cls.graph_usuage, label='Used Space', marker='.')
        plt.legend()
        plt.savefig('./Graph1.png')
        ar = [cls.graph_day, cls.graph_usuage]
        cls.update(ar)

    # this method clears the temp file
    @classmethod
    def clear_mem(cls):
        os.remove('./DiskUsuage.txt')

    # this method makes it easier to run each of the methods of the class in order.
    @classmethod
    def main_run(cls):
       cls.read_sys()       
       cls.check_prev()
       cls.read_data()
       cls.save_data()
       cls.clear_mem()
