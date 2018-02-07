import sys

hid = { 30: '1', 31: '2', 32: '3', 33: '4', 34: '5', 35: '6', 36: '7', 37: '8', 38: '9', 39: '0' }

fp = open('/dev/hidraw0', 'rb')

while 1:
    ss = ""
    done = False
    while not done:
        buffer = fp.read(11)
        for c in buffer:
            if c > 0:
                if c == 40:
                    done = True
                    break;
                ss += hid[c]
    print(ss)
