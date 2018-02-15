import re
from datetime import datetime

pattern_date = r'[0-9]{1,3}/[a-zA-Z]{1,4}/[0-9]{1,5}:[0-9]{1,3}:[0-9]{1,3}:[0-9]{1,3}'

def log_manipulation(filename):
    '''
    This function takes logfile name as input and searches for date and time in any logfile entry and if entry is
    more than 3 days old. It will delete that entry.
    :param filename:
    :return:
    '''
    diffarr = []
    with open(filename,'r+') as outfile:
        buffer = outfile.readlines()
        for line,buff in enumerate(buffer):
            date_time = re.findall(pattern_date,buff )
            date_time_formatted = datetime.strptime(str(date_time[0]), "%d/%b/%Y:%H:%M:%S")
            curr_time = datetime.now()
            delta = (curr_time-date_time_formatted).days
            if delta<=3:
                diffarr.append(buff)

    with open(filename, 'w') as outfile:
        for i in diffarr:
            outfile.write(i)

log_manipulation(filename="ssl_access_logs")





