import sys
from httplib2 import Http

def get_status_code(path):
    h = Http()
    resp, content = h.request(path, "GET")
    return resp.status

def get_card_number():
    # translate numbers
    hid = { 30: '1', 31: '2', 32: '3', 33: '4', 34: '5', 35: '6', 36: '7', 37: '8', 38: '9', 39: '0' }

    print("Swipe your card: ")
    if sys.platform == "linux" or sys.platform == "linux2":
        fp = open('/dev/hidraw0', 'rb')

        ss = ""
        done = False
        while not done:
            buffer = fp.read(11)
            for c in buffer:
                if c > 0:
                    if c == 40:
                        # 40 means the current card number is done
                        done = True
                        break
                    ss += hid[c]
    elif sys.platform == "win32":
        ss = str(input())
    else:
        ss = 0
        print("Unfortunately your system is not supported")

    return ss

while 1:
    ss = get_card_number()
    print(ss)
    if(get_status_code("http://kort.codingpirates.dk/checkin/" + ss) == 200):
        print("success")
