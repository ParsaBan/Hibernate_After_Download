import os
import time

import psutil

UPDATE_DELAY = 1 # in seconds
check = 0

def get_size(bytes):
    """
    Returns size of bytes in a nice format
    """
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}B"
        bytes /= 1024

# get the network I/O stats from psutil
io = psutil.net_io_counters()
# extract the total bytes sent and received
bytes_sent, bytes_recv = io.bytes_sent, io.bytes_recv

while True:
    # if a timer has been started, check if it has been 10 seconds of minimal download speed, hibernate if so
    try: 
        if (time.time() - start > 10):
            os.system(r'%windir%\system32\rundll32.exe powrprof.dll,SetSuspendState Hibernate')
            break
    except:
        pass

    # sleep for `UPDATE_DELAY` seconds
    time.sleep(UPDATE_DELAY)
    # get the stats again
    io_2 = psutil.net_io_counters()
    # new - old stats gets us the speed
    us, ds = io_2.bytes_sent - bytes_sent, io_2.bytes_recv - bytes_recv
    print(f"Upload: {get_size(io_2.bytes_sent)}   "
          f", Download: {get_size(io_2.bytes_recv)}   "
          f", Upload Speed: {get_size(us / UPDATE_DELAY)}/s   "
          f", Download Speed: {get_size(ds / UPDATE_DELAY)}/s      ", end="\r")
    # update for next iteration
    bytes_sent, bytes_recv = io_2.bytes_sent, io_2.bytes_recv
    
    #if download speed is less than 10 KB, start a timer
    if (not check and ds < 250 * 1024):
        start = time.time()
        check = 1
    

