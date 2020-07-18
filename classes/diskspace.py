import os
import subprocess
from matplotlib import pyplot as plt
from matplotlib import dates
from matplotlib import axes
import datetime
import time
import pickle


class Disk(object):
    #Graph Settings
    STYLE = 'solid' #linestyle in the plot_date method
    GRAPH_STYLE = 'dark_background' #check available styles using plt.style.availabe

    #variables used
    graph_usuage = []
    graph_date = []
    drive_info = {}
    # this runs the df -h command on terminal and pipes the output to a temp
    # file
    @classmethod
    def read_sys(cls):
        path = os.getcwd()
        with open(os.path.join(path, 'classes/Config/DiskUsuage.txt'), 'w') as f:
            file_data = subprocess.run('df -h', shell=True, text=True, stdout=f)
        del path

    # this appends all the relavent info to the drive_info dictionary which is
    # used to retrive total/used space in the main.py file
    @classmethod
    def ret_fun(cls, **kwargs):
        for arg, value in kwargs.items():
            cls.drive_info.update({arg: value})

    # this method read the output for the read_sys file where each line
    # corresponds to a drive
    @classmethod
    def read_data(cls):
        path = os.getcwd()

        with open(os.path.join(path, 'classes/Config/DiskUsuage.txt'), 'r') as f:
            a = f.readlines()

        check = len(a)

        for i in range(check):
            # 3 because df -h returns the output for temp folders which in this
            # case is not required (for me)
            i += 1

            # 0:2 for windows # Parsing throught the string to get only  drive
            # name
            drive = a[i][0:2]
            # 0:9 for linux

            # 16:19 for windows and linux #Parsing throught the string to get
            # only the total memory allocated
            total = int(a[i][16:19])

            # 23:25 for windows #Parsing throught the string to get only the
            # used memory
            used = float(a[i][23:25])
            # 22:25 for linux

            year = time.localtime().tm_year
            month = time.localtime().tm_mon
            day = time.localtime().tm_mday 

            # TODO: Make the plot better 
            date = datetime.datetime(year, month, day)
            '''
            Year day over month day because at the start of each month the x-axis becomes 0; this causes a hard to read graph

            A possible and simple solution is to make multiple graphs and append them to a single plot to differentiate the different months
            which will probably be added in upcoming versions
            '''

            # appending to graph_date / graph_usuage so that it can reatain info
            # about the current state whenever it is called.
            if(os.path.exists(os.path.join(path, 'classes/Config/storage.info'))):
                cls.graph_date.append(date)
                cls.graph_usuage.append(used)
            else:
                start_date = datetime.datetime(2020, 7, 18)
                cls.graph_date.append(start_date)
                cls.graph_usuage.append(0)
                cls.graph_date.append(date)
                cls.graph_usuage.append(used)
            # print(f'Drive: {drive}, Total Space: {total} GB ,Used Space:
            # {used} GB, Available: {total - used} GB, % Used: {int((lambda :
            # (used/total)*100)())} %')
            cls.ret_fun(drive=drive, total=total, used=used)
            del path
            break

    '''
    the storage.info file contains a single array in the format of;
    [<day>,<space used>]

    which overtime increases as;

    [[<day>,<space used>],[<day1>,<space used1>],[<day2>,<space used2>],[<day3>,<space used3>]]
    '''

    # this is used to update the array stored in the storage.info file so that
    # the space used and day/time are retrived and plotted as necessary
    @classmethod
    def update(cls, ar):
        path = os.getcwd()
        with open(os.path.join(path, 'classes/Config/storage.info'), 'wb') as f:
            pickle.dump(ar, f)
        del path

    # checks the previous saved data and add it to the graph_date,graph_usuage
    # list to be plotted again
    @classmethod
    def check_prev(cls):
        path = os.getcwd()

        if(os.path.exists(os.path.join(path, 'classes/Config/storage.info'))):
            with open(os.path.join(path, 'classes/Config/storage.info'), 'rb') as file:
                data_ = pickle.load(file)

            for date_ in data_[0]:
                cls.graph_date.append(date_)
            for usuage_ in data_[1]:
                cls.graph_usuage.append(usuage_)

        del path

    # this method plots the graph using matplotlib
    @classmethod
    def save_data(cls):
        path = os.getcwd()
        plt.style.use(cls.GRAPH_STYLE)
        plt.title('Server Disk Usuage')
        plt.xlabel('Date --->')
        plt.ylabel('Space Used (GB)--->')

        plt.plot_date(cls.graph_date, cls.graph_usuage,label='Used Space',linestyle=cls.STYLE)

        plt.gcf().autofmt_xdate()

        plt.xlim(cls.graph_date[0])
        plt.ylim(0)

        format = dates.DateFormatter('%Y %b %d')
        plt.gca().xaxis.set_major_formatter(format)
        plt.tight_layout()
        plt.legend()

        plt.savefig(os.path.join(path,'classes/Config/Graph.png'))
        array = [cls.graph_date, cls.graph_usuage]
        cls.update(array)

    # this method clears the temp file
    @classmethod
    def clear_mem(cls):
        path = os.getcwd()
        os.remove(os.path.join(path, 'classes/Config/DiskUsuage.txt'))
    

    # this method makes it easier to run each method of the class in
    # order.
    @classmethod
    def main_run(cls):
        cls.read_sys()
        cls.check_prev()
        cls.read_data()
        cls.save_data() #also updates the previous
        cls.clear_mem()
