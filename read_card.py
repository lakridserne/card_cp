import sys
from urllib.request import urlopen
from urllib.error import URLError, HTTPError


def get_status_code(path):
    try:
        response = urlopen(path)
        return response.getcode()
    except HTTPError as e:
        print(
            "Arrrrrrrrrr! Noget gik galt. Find Kristoffer og sig ", e.code, " til ham!"
        )
    except URLError as e:
        print(
            "Arrrrrrrrrr! Noget gik galt! Find Kristoffer og sig ",
            e.reason,
            " til ham!",
        )


def get_card_number():
    # translate numbers
    hid = {
        30: "1",
        31: "2",
        32: "3",
        33: "4",
        34: "5",
        35: "6",
        36: "7",
        37: "8",
        38: "9",
        39: "0",
    }

    print("Vis mig dit kort!")
    if sys.platform == "linux" or sys.platform == "linux2":
        with open("/dev/hidraw0", "rb") as fp:
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
    if get_status_code("https://kort.codingpirates.dk/checkin/" + ss + "/") == 200:
        print("Ahoy me hearties! Velkommen ombord på skibet! Arrrrrrrr!!!")
