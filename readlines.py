import serial
import sys


def line_str(s):
    s = s.replace('\r\n', '')
    return s


def main(serial_port):
    ser = serial.Serial(serial_port, 115200)
    cnt = 0
    data = ser.readline()
    while data:
        line = data.decode()
        cnt += 1
        print('%03d ' % cnt, line_str(line))
        data = ser.readline()
    ser.close()

if len(sys.argv) < 2:
    print(f'{sys.argv[0]} serial_port')
else:
    main(sys.argv[1])
