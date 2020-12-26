from log import message
message("Main.py start")
def main():
    message("Main function start")
    from miscellaneous import read_json
    from networkManager import network_handler
    from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
    from hardware import setup_components, calibrate_sensor, DS04NFC, update_display
    from log import debugging
    components = setup_components(read_json("data/config")["components"])
    components["button"]["previousState"] = False
    robbery_active = False
    components["led"]["object"].off()
    components["motor"]["object"].stop()
    components["speaker"]["object"].stop()
    components["laser"]["object"].off()
    calibrate_sensor(components)
    s = socket(AF_INET, SOCK_STREAM)
    s.settimeout(1)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(('', 80))
    s.listen(5)
    while True:
        import gc
        gc.collect()
        try:
            connection_socket, address = s.accept()
            print('Got a connection from %s' % str(address))
            network_handler(connection_socket, components, robbery_active)
        except OSError:
            debugging("Socket timeout")
        if not robbery_active:
            robbery_active = normal_activity(components)
            if components["configButton"]["object"].value() == 1:
                from utime import sleep
                message("Config button pressed")
                sleep(3)
                calibrate_sensor(components)
                update_display(components)
                sleep(3)
        elif components["configButton"]["object"].value() == 1:
            from log import warning
            from machine import Pin
            warning("Robbery state turned off by config button")
            update_display(components)
            components["led"]["object"].off()
            DS04NFC(Pin(2, Pin.OUT)).stop()
            components["speaker"]["object"].stop()
            robbery_active = False
def normal_activity(components: dict) -> bool:
    from log import debugging, warning, repeat_message
    if components["button"]["object"].value() == 1 and not components["button"]["previousState"]:
        components["button"]["previousState"] = True
        if components["led"]["object"].value() == 0:
            components["led"]["object"].on()
            debugging("Turned led on")
        if components["laser"]["object"].value() == 0:
            components["laser"]["object"].on()
            warning("Turned laser on")
    elif components["button"]["object"].value() == 0 and components["button"]["previousState"]:
        components["button"]["previousState"] = False
        if components["led"]["object"].value() == 1:
            components["led"]["object"].off()
            debugging("Turned led off")
        if components["laser"]["object"].value() == 1:
            components["laser"]["object"].off()
            warning("Turned laser off")
    try:
        if components["lightSensor"]["object"].read() > components["lightSensor"]["thresholdSensitivity"] and \
                components["button"]["object"].value() == 1:
            repeat_message("Laser on light sensor", 10, "laser on light")
        elif components["button"]["object"].value() == 1:
            warning("A robbery has been detected")
            robbery_activity(components)
            return True
    except KeyError:
        warning("ThresholdSensitivity has not been calibrated")
    return False
def robbery_activity(components: dict):
    from hardware import update_display
    components["led"]["object"].on()  # Turn led on
    components["motor"]["object"].forward(components["motor"]["speed"])  # Turn motor on
    components["speaker"]["object"].alarm()  # Turn speaker on
    components["laser"]["object"].off()  # Turn laser off
    update_display(components, "robbery", ["", "There is", "a robbery."])  # Update display with message
if __name__ == '__main__':  # Check if python is ready
    main()
else:
    from log import error
    error("Main failed")
