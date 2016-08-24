import datetime
import time
import configparser
import json
import schedule
import psutil

txt_name = 'monitor.txt'
json_name = 'monitor.json'
snapshot = 0

conf = configparser.ConfigParser()
conf.read('settings.ini')
output = conf.get('common', 'output')
interval = conf.get('common', 'interval')


class test1:
    def tmp(self):
        tm = time.time()
        timestamp = datetime.datetime.fromtimestamp(tm).strftime('%Y-%m-%d %H:%M:%S')
        return timestamp


class text (test1):
    def textfile(self, filename='monitor.txt'):
        global snapshot
        snapshot += 1
        f = open(filename, 'a+')
        f.write('\nSnapshot {0}:{1}\n'.format(snapshot, self.tmp()))
        f.write('CPU load: {0} %\n'.format(psutil.cpu_percent(percpu=True)))
        f.write('Overall memory usage: {0} Mb\n'.format(
            (str((psutil.virtual_memory().used / 1024 / 1024).__round__(2)))))
        f.write('Overall virtual memory usage: {0} Mb\n'.format(
            (str((psutil.swap_memory().used / 1024 / 1024).__round__(2)))))
        f.write('MB read: {0} Mb, MB written: {1} Mb\n'.format(
            (str((psutil.disk_io_counters()[0] / 1024 / 1024).__round__(2))),
            (str((psutil.disk_io_counters()[1] / 1024 / 1024).__round__(2)))))
        f.write('MB sent: {0} Mb, MB received: {1} Mb\n'.format(
            (str((psutil.net_io_counters(pernic=False)[0] / 1024 / 1024).__round__(2))),
            (str((psutil.net_io_counters(pernic=False)[1] / 1024 / 1024).__round__(2)))))
        f.close()


class test2(test1):
    def jsonfile(self, filename='monitor.json'):
        global snapshot
        snapshot += 1
# creating dictionary to store monitoring information
        monitor = {
            'CPU load': psutil.cpu_percent(percpu=True),
            'Overall memory usage': psutil.virtual_memory().used,
            'Overall virtual memory usage': psutil.swap_memory().used,
            'IO information': [psutil.disk_io_counters()[0], psutil.disk_io_counters()[1]],
            'Nework information': [psutil.net_io_counters(pernic=False)[0], psutil.net_io_counters(pernic=False)[1]]
            }
# setting information format
        data = ['SNAPSHOT ' + str(snapshot) + ': ' + str(self.tmp()), monitor]
# writing data to json
        with open(filename, 'a+') as j:
            json.dump(data, j, indent=4, sort_keys=True)

out_text = text()

out_json = test2()


def out():
    if output == 'txt':
        out_text.textfile()
    elif output == 'json':
        out_json.jsonfile()

schedule.every(int(interval)).seconds.do(out)

while True:
    schedule.run_pending()
