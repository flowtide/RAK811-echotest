import serial
import sys


def line_str(s):
    s = s.replace('\r\n', '')
    return s


def main(serial_port, text):
    ser = serial.Serial(serial_port, 115200, timeout=0.5)
    data = text + '\r\n'
    print('>>', line_str(data))
    ser.write(data.encode())
    cnt = 0
    data = ser.readline()
    while data:
        line = data.decode()
        cnt += 1
        print('%03d ' % cnt, line_str(line))
        data = ser.readline()
    ser.close()


if len(sys.argv) < 3:
    print(f'{sys.argv[0]} serial_port text')
else:
    main(sys.argv[1], sys.argv[2])
