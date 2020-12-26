from log import warning, message
from gc import enable
print("\033[92m(days:0, hr:0, min:0, s:0) LOG: Boot.py start\033[0m")
enable()
print("\033[92m(days:0, hr:0, min:0, s:0) LOG: Garbage collector has been enabled\033[0m")
def connect_to_network():
    from network import WLAN, STA_IF, AP_IF
    from miscellaneous import read_json
    sta_if = WLAN(STA_IF)
    ap_if = WLAN(AP_IF)
    if read_json("data/config")["network"]["networkStation"]["enabled"] is True:
        from time import time
        warning("Network station will be enabled")
        if sta_if.isconnected():
            message('Already connected to network')
        while not sta_if.isconnected():
            message('Connecting to network...')
            sta_if.active(True)
            if read_json("data/config")["network"]["networkStation"]["homeNetwork"] is True:
                warning("Using home network")
                sta_if.connect('Hackercollective', 'w6HSB2S3bb042')
            else:
                warning("Using custom network config")
                ssid = read_json("data/config")["network"]["networkStation"]["customSSID"]
                password = read_json("data/config")["network"]["networkStation"]["customNetworkPassword"]
                sta_if.connect(ssid, password)
            start_time = time() + 120
            while not sta_if.isconnected():
                if time() == start_time:
                    break
        message('Network config:' + str(sta_if.ifconfig()))
        message('The ip is ' + str(sta_if.ifconfig()[0]))
    else:
        warning("Network station will be disabled")
        sta_if.active(False)
    if read_json("data/config")["network"]["accessPoint"]["enabled"] is True:
        warning("Access point will be enabled")
        ap_if.active(True)
        ap_if.config(essid=read_json("data/config")["network"]["accessPoint"]["SSID"],
                     password=read_json("data/config")["network"]["accessPoint"]["password"])
    else:
        warning("Access point will be disabled")
        ap_if.active(False)
def set_start_time():
    from utime import mktime, localtime
    from miscellaneous import write_json, read_json
    from log import message
    json_dict = read_json("data/config")
    json_dict["dumpJson"]["startTime"] = mktime(localtime())
    write_json("data/dump", json_dict["dumpJson"])
    message("Start time set")
if __name__ == '__main__':
    set_start_time()
    connect_to_network()
else:
    from log import error
    error("Boot failed")
