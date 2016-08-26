import datetime
import time
import configparser
import json
import schedule
import psutil


# setting output files names
txt_name = 'monitor.txt'
json_name = 'monitor.json'
snapshot = 0


# reading settings from configuration file
conf = configparser.ConfigParser()
conf.read('settings.ini')
output = conf.get('common', 'output')
interval = conf.get('common', 'interval')
trace_enabled = conf.getboolean('common', 'decorator')


# decorator
def trace(func):
    def wrapper(*args, **kwargs):
        t = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        a = open('test.log', 'a+')
        a.write('Enter: ' + str(t) + '\n' + func.__name__ + ', arguments: ' + str(args) + '\n')
        func(*args, **kwargs)
        a.write('Exit: ' + func.__name__ + '\n' + '\n')
        a.close()
        return(func(*args, **kwargs))
    return wrapper if trace_enabled else func


class test1:
    # setting atributes to object
    def __init__(self):
        self.cpu = ('CPU load: '+str(psutil.cpu_percent(0, 0))+' %')
        self.mem = ('Overall memory usage: '+str((psutil.virtual_memory().used/1024/1024).__round__(2))+' Mb')
        self.swap = ('Virtual memory usage: '+str((psutil.swap_memory().used/1024/1024).__round__(2))+' Mb')
        self.io_read = ('Mb read from disk: '+str((psutil.disk_io_counters()[3]/1024/1024).__round__(2)))
        self.io_write = ('Mb written to disk: '+str((psutil.disk_io_counters()[4]/1024/1024).__round__(2)))
        self.network_sent = ('Mb sent: '+str((psutil.net_io_counters(pernic=False)[0]/1024/1024).__round__(2)))
        self.network_received = ('Mb received: ' + str((psutil.net_io_counters(pernic=False)[1] / 1024 / 1024).__round__(2)))
        tm = time.time()
        self.timestamp = datetime.datetime.fromtimestamp(tm).strftime('%Y-%m-%d %H:%M:%S')


class text (test1):
    def __init__(self):
        super().__init__()

    @trace
    def textfile(self, filename='monitor.txt'):
        global snapshot
        snapshot += 1
        f = open(filename, 'a+')
        f.write('Snapshot {0}:{1}'.format(snapshot, self.timestamp))
        f.write('\n' + self.cpu)
        f.write('\n' + self.mem)
        f.write('\n' + self.swap)
        f.write('\n' + self.io_read)
        f.write('\n' + self.io_write)
        f.write('\n' + self.network_sent)
        f.write('\n' + self.network_received + '\n'+'\n')
        f.close()


class test2(test1):
    def __init__(self):
        super().__init__()

    @trace
    def jsonfile(self, filename='monitor.json'):
        global snapshot
        snapshot += 1
# creating dictionary to store monitoring information
        monitor = [self.cpu, self.mem, self.swap, self.io_read, self.io_write, self.network_sent, self.network_received]
# setting information format
        data = ['SNAPSHOT ' + str(snapshot) + ': ' + str(self.timestamp), monitor]
# writing data to json
        with open(filename, 'a+') as j:
            json.dump(data, j, indent=4, sort_keys=True)


def out():
    if output == 'txt':
        out_text = text()
        out_text.textfile()
    elif output == 'json':
        out_json = test2()
        out_json.jsonfile()
    else:
        quit()

schedule.every(int(interval)).seconds.do(out)

while True:
    schedule.run_pending()
