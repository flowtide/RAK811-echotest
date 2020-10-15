import re
from collections import namedtuple

## RAK811 echo server
# ser.readline() returns data like following.
# "at+recv=-10,6,10:12345678901234567890"
# when ever it receive valid data it echos like following.
# "at+send=lorap2p:12345678901234567890"

AtCommandLine = namedtuple('CommandLine', ['cmd', 'rssi', 'snr', 'data_len', 'data'])

def parse_at_command(line):
    """ parsing: at+recv=<RSSI>,<SNR>,< Data Length >:< Data > """
    result = re.match(r'at\+(\w+)=(-?\d+),(-?\d+),(\d+):(.+[^\r\n])', line)
    if result:
        #print(f'groups: {result.groups()} 0: {result.group(0)}')
        return AtCommandLine(result.group(1), int(result.group(2)), int(result.group(3)), int(result.group(4)), result.group(5))

