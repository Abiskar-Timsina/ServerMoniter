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
    password = #<Your login password for the associated gmail>
    
    @classmethod
    def read_sys(cls):
        with open('./DiskUsuage.txt', 'w') as f:
            file_data = subprocess.run(
                'df -h', shell=True, text=True, stdout=f)

    @classmethod        
    def ret_fun(cls,**kwargs):
        for arg,value in kwargs.items():
            cls.drive_info.update({arg:value})


    @classmethod
    def read_data(cls):
        with open('./DiskUsuage.txt', 'r') as f:
            a = f.readlines()

        check = len(a)

        for i in range(check):
            i += 3

            drive = a[i][0:9] #0:2 for windows
 
            total = int(a[i][16:19]) #16:19 for windows

            used = float(a[i][22:25]) #23:25 for windows

            day = time.localtime().tm_yday

            cls.graph_day.append(day)
            cls.graph_usuage.append((used))
            # print(f'Drive: {drive}, Total Space: {total} GB ,Used Space: {used} GB, Available: {total - used} GB, % Used: {int((lambda : (used/total)*100)())} %')
            cls.ret_fun(drive=drive,total=total,used=used)
            break



    @classmethod
    def update(cls, ar):
        with open('./info.config', 'wb') as f:
            pickle.dump(ar, f)

    @classmethod
    def check_prev(cls):
	    if(os.path.exists('./info.config')):
	        with open('./info.config', 'rb') as file:
	            data = pickle.load(file)

	        for d in data[0]:
	            cls.graph_day.append(d)
	        for u in data[1]:
	            cls.graph_usuage.append(u)

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

    @classmethod
    def clear_mem(cls):
        os.remove('./DiskUsuage.txt')

    @classmethod
    def main_run(cls):
       cls.read_sys()       
       cls.check_prev()
       cls.read_data()
       cls.save_data()
       cls.clear_mem()
