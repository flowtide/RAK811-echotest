import serial, sys
import at_command
from datetime import datetime
import random
import timeit
import time

## RAK811 echo test program:
# This program is to check TX/RX throughput RAK811 Lora breakout module.
# It sends random data to peer by AT command
# and checks echo response.

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
    data = ser.readline() # read 'OK'
    if data != b'OK \r\n':
        print('at+set_config failed:', data.decode() if data else '<NO RESPONSE>')
    else:
        return True

def main(serial_port, packet_size, num_test, interval):
    ser = serial.Serial(serial_port, 115200, timeout=1)
    cnt = 0
    ok = 0
    start_at = timeit.default_timer()
    total_bytes = 0
    while cnt < num_test:
        cnt += 1
        set_transfer_mode(ser, 2)
        tx_data = bytes([random.randrange(0, 256) for _ in range(0, packet_size)]).hex().upper()
        send(ser, tx_data)
        tx_at = timeit.default_timer()
        # wait for echo response
        set_transfer_mode(ser, 1)
        data = ser.readline()
        delay = timeit.default_timer() - tx_at
        if data:
            at_cmd = at_command.parse_at_command(data.decode())
            if at_cmd:
                if at_cmd.cmd == 'recv':
                    if tx_data == at_cmd.data:
                        ok += 1
                        total_bytes += packet_size * 2 # multiplied by 2 because TX/RX roundtrip
                        print('%s %04d/%04d DELAY=%.3f BPS=%.2f RSSI=%d SNR=%d LEN=%3d MATCH' % (datetime.now().strftime('%H:%M:%S.%f'), ok, cnt, delay,
                            total_bytes * 8 / (timeit.default_timer() - start_at),
                            at_cmd.rssi, at_cmd.snr, at_cmd.data_len))
                    else:
                        print('%s %04d/%04d DELAY=%.3f RSSI=%d SNR=%d LEN=%3d NOT MATCH' % (datetime.now().strftime('%H:%M:%S.%f'), ok, cnt, delay, at_cmd.rssi, at_cmd.snr, at_cmd.data_len))
                        print('TX data:', tx_data)
                        print('RX data:', at_cmd.data)
            else:
                print(f'unknown read data: {data.decode()}')
        else:
            print('%s %04d timeout' % (datetime.now().strftime('%H:%M:%S.%f'), cnt))
        total_delay = timeit.default_timer() - tx_at
        if total_delay < interval:
            time.sleep(interval - total_delay)
    ser.close()


if len(sys.argv) < 4:
    print(f'{sys.argv[0]} serial_port packet_size test_num interval')
else:
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]))
