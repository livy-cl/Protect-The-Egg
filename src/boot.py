from log import warning, message
from gc import enable  # enable the garbage collector

print("\033[92m(days:0, hr:0, min:0, s:0) LOG: Boot.py start\033[0m")

enable()
print("\033[92m(days:0, hr:0, min:0, s:0) LOG: Garbage collector has been enabled\033[0m")


def connect_to_network():
    """
    connect to a network and disable the access point
    """
    from network import WLAN, STA_IF, AP_IF
    from miscellaneous import read_json

    sta_if = WLAN(STA_IF)  # wifi station (connect to router)
    ap_if = WLAN(AP_IF)  # wifi access point (like a router)

    if read_json("data/config")["network"]["networkStation"]["enabled"] is True:
        warning("Network station will be enabled")

        if sta_if.isconnected():  # check if you're already connected
            message('Already connected to network')

        while not sta_if.isconnected():
            message('Connecting to network...')

            sta_if.active(True)  # enable the station

            if read_json("data/config")["network"]["networkStation"]["homeNetwork"] is True:  # check if you want to
                # connect to home wifi
                warning("Using home network")
                sta_if.connect('Hackercollective', 'w6HSB2S3bb042')  # let station connect to wifi
            else:  # connect to custom wifi
                warning("Using custom network config")
                ssid = read_json("data/config")["network"]["networkStation"]["customSSID"]  # read custom wifi ssid
                # from json
                password = read_json("data/config")["network"]["networkStation"]["customNetworkPassword"]  # read
                # custom password from json
                sta_if.connect(ssid, password)  # let station connect to wifi

            from time import time  # import time to make a timer
            start_time = time() + 120  # make timer (last value is how long the timer in ms)
            while not sta_if.isconnected():  # wait to be connected
                if time() == start_time:  # check if timer is over
                    break

        message('Network config:' + str(sta_if.ifconfig()))
        message('The ip is ' + str(sta_if.ifconfig()[0]))
    else:
        warning("Network station will be disabled")
        sta_if.active(False)  # enable network station

    if read_json("data/config")["network"]["accessPoint"]["enabled"] is True:  # check if you want an access point in
        # config
        warning("Access point will be enabled")
        ap_if.active(True)  # disable access point

        ap_if.config(essid=read_json("data/config")["network"]["accessPoint"]["SSID"],  # set password and ssid of
                     password=read_json("data/config")["network"]["accessPoint"]["password"])  # the access point

    else:
        warning("Access point will be disabled")
        ap_if.active(False)  # enable access point


def set_start_time():
    """
    saves the time of the start of the program so that time can be used to calculate how many seconds the programs has
    been running
    """
    from utime import mktime, localtime
    from miscellaneous import write_json, read_json
    from log import message

    json_dict = read_json("data/config")  # read config json file (so i can later save it to dump json file)
    json_dict["dumpJson"]["startTime"] = mktime(localtime())  # set starTime equal to current time
    write_json("data/dump", json_dict["dumpJson"])  # save dictionary to the json file dump

    message("Start time set")


if __name__ == '__main__':  # check if python is ready
    set_start_time()
    connect_to_network()
else:
    from log import error
    error("Boot failed")
