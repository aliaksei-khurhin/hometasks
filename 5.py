import psutil, datetime, time, configparser,json, schedule

txt_name = 'monitor.txt'
json_name = 'monitor.json'

#getting information from config file
conf = configparser.ConfigParser()
conf.read('settings.ini')
output = conf.get('common', 'output')
interval = conf.get('common', 'interval')

snapshot = 0

#function to write information to txt file
def textfile():
    global snapshot
    global txt_name
    snapshot += 1
    tm = time.time()
    timestamp = datetime.datetime.fromtimestamp(tm).strftime('%Y-%m-%d %H:%M:%S')
    f = open(txt_name, 'a+')
    f.write('\nSnapshot {0}:{1}\n'.format(snapshot, timestamp))
    f.write('CPU load: {0} %\n'.format(psutil.cpu_percent(percpu=True)))
    f.write('Overall memory usage: {0} Mb\n'.format((str((psutil.virtual_memory().used / 1024 / 1024).__round__(2)))))
    f.write('Overall virtual memory usage: {0} Mb\n'.format((str((psutil.swap_memory().used/1024/1024).__round__(2)))))
    f.write('MB read: {0} Mb, MB written: {1} Mb\n'.format(
        (str((psutil.disk_io_counters()[0]/1024/1024).__round__(2))),
        (str((psutil.disk_io_counters()[1]/1024/1024).__round__(2)))))
    f.write('MB sent: {0} Mb, MB received: {1} Mb\n'.format(
        (str((psutil.net_io_counters(pernic=False)[0] / 1024 / 1024).__round__(2))),
        (str((psutil.net_io_counters(pernic=False)[1] / 1024 / 1024).__round__(2)))))


#function to write information to txt file
def jsonfile():
    global snapshot
    global json_name
    snapshot += 1

#creating dictionary to store monitoring information
    monitor = {
        'CPU load': psutil.cpu_percent(percpu=True),
        'Overall memory usage': psutil.virtual_memory().used,
        'Overall virtual memory usage': psutil.swap_memory().used,
        'IO information': [psutil.disk_io_counters()[0],psutil.disk_io_counters()[1]],
        'Nework information': [psutil.net_io_counters(pernic=False)[0],psutil.net_io_counters(pernic=False)[1]]
    }
#setting information format
    data = ['SNAPSHOT ' + str(snapshot) + ': ' + str(timestamp), monitor]
#writiong data to json
    with open(json_name, 'a+') as j:
        json.dump(data, j, indent=4, sort_keys=True)


if output == 'txt':
    schedule.every(int(interval)).seconds.do(textfile)
elif output == 'json':
    schedule.every(int(interval)).seconds.do(jsonfile)
else:
    print("Incorrect output format, please specify *.txt or *.json output format")
    quit()

while True:
    schedule.run_pending()