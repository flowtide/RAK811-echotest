import serial, sys, time
from at_command import parse_at_command
from datetime import datetime

## RAK811 echo server
# ser.readline() returns data like following.
# "at+recv=-10,6,10:12345678901234567890"
# whenever it receive valid data it sends back like following.
# "at+send=lorap2p:12345678901234567890"

def send(ser, line):
    ''' RX mode: 1, TX mode: 2'''
    tx_cmd = f'at+send=lorap2p:{line}\r\n'
    ser.write(tx_cmd.encode())
    data = ser.readline() # read 'OK'
    if data != b'OK \r\n':
        print('at+send failed:', data.decode() if data else '<NO RESPONSE>')
    else:
        return True


def set_transfer_mode(ser, mode):
    ''' RX mode: 1, TX mode: 2'''
    tx_cmd = f'at+set_config=lorap2p:transfer_mode:{mode}\r\n'
    ser.write(tx_cmd.encode())
    data = ser.readline() # read 'ok'
    if data != b'OK \r\n':
        print('set_transfer_mode failed:', data.decode())
    else:
        return True


def main(serial_port):
    ser = serial.Serial(serial_port, 115200)
    cnt = 0
    if set_transfer_mode(ser, 1):
        print('set transfer_mode RX')
    else:
        return
    data = ser.readline()
    while data:
        at_cmd = parse_at_command(data.decode())
        if at_cmd:
            if at_cmd.cmd == 'recv':
                assert at_cmd.data_len * 2 == len(at_cmd.data) ## lengh of data is double because AT command data is hexdecial values.
                cnt += 1
                print('%s %04d RSSI=%d SNR=%d LEN=%3d' % (datetime.now().strftime('%H:%M:%S.%f'), cnt, at_cmd.rssi, at_cmd.snr, at_cmd.data_len), at_cmd.data)
                set_transfer_mode(ser, 2)
                send(ser, at_cmd.data)
                set_transfer_mode(ser, 1)
        else:
            print(f'unknown read data: {data.decode()}')
        data = ser.readline()
    ser.close()


if len(sys.argv) < 2:
    print(f'{sys.argv[0]} serial_port')
else:
    main(sys.argv[1])
