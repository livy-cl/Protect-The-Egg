from log import message
message("Main.py start")


def main():
    message("Main function start")
    from miscellaneous import read_json
    from networkManager import network_handler
    from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
    from hardware import setup_components, calibrate_sensor, DS04NFC, update_display
    from log import debugging

    components = setup_components(read_json("data/config")["components"])  # initialize all the components
    components["button"]["previousState"] = False
    robbery_active = False  # This is true if there is a robber

    components["led"]["object"].off()  # turn led off
    components["motor"]["object"].stop()  # turn motor off
    components["speaker"]["object"].stop()  # turn speaker off
    components["laser"]["object"].off()  # turn laser off

    calibrate_sensor(components)  # calibrate the sensor

    s = socket(AF_INET, SOCK_STREAM)  # make a socket (=give access to the BSD socket interface)
    s.settimeout(1)  # accept function will timeout after 1 second
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # check and filter outgoing packages
    s.bind(('', 80))  # bind socket to localhost and port 80 (=localhost:80 or http://localhost)
    s.listen(5)  # listen to the bounded address

    while True:
        import gc
        gc.collect()  # collect garbage
        try:
            connection_socket, address = s.accept()  # wait for user to accept socket
            print('Got a connection from %s' % str(address))

            network_handler(connection_socket, components, robbery_active)  # a function that handles network usages
        except OSError:  # a result of settimeout(1) see line 24
            debugging("Socket timeout")

        if not robbery_active:  # check if there is no robbery
            robbery_active = normal_activity(components)  # execute the normal events
            if components["configButton"]["object"].value() == 1:  # check config button
                from utime import sleep
                message("Config button pressed")
                sleep(3)  # wait for 3 seconds
                calibrate_sensor(components)  # calibrate sensor again
                update_display(components)  # clear the display
                sleep(3)  # wait for 3 seconds
        elif components["configButton"]["object"].value() == 1:  # there is a robbery and the config button is pressed
            from log import warning
            from machine import Pin

            warning("Robbery state turned off by config button")
            update_display(components)  # clear display
            components["led"]["object"].off()  # turn led off
            DS04NFC(Pin(2, Pin.OUT)).stop()  # turn motor off
            components["speaker"]["object"].stop()  # turn speaker off
            robbery_active = False  # set robbery variable to no robbery


def normal_activity(components: dict) -> bool:
    from log import debugging, warning, repeat_message

    if components["button"]["object"].value() == 1 and not components["button"]["previousState"]:  # Button pressed and
        # previous state is false
        components["button"]["previousState"] = True  # Turn previous state to true for next run time
        if components["led"]["object"].value() == 0:  # Check if led is off (so it does not turn it on when it is on)
            components["led"]["object"].on()  # Turn led on
            debugging("Turned led on")
        if components["laser"]["object"].value() == 0:  # Check if laser is off
            components["laser"]["object"].on()  # Turn laser on
            warning("Turned laser on")
    elif components["button"]["object"].value() == 0 and components["button"]["previousState"]:  # If button is not
        # pressed and previous state is true
        components["button"]["previousState"] = False  # Turn previous state to false for next run time
        if components["led"]["object"].value() == 1:  # Check if led is on
            components["led"]["object"].off()  # Turn led off
            debugging("Turned led off")
        if components["laser"]["object"].value() == 1:  # Check if laser is on
            components["laser"]["object"].off()  # Turn laser on
            warning("Turned laser off")
    try:
        if components["lightSensor"]["object"].read() > components["lightSensor"]["thresholdSensitivity"] and \
                components["button"]["object"].value() == 1:  # Laser on sensor and button pressed
            repeat_message("Laser on light sensor", 10, "laser on light")
        elif components["button"]["object"].value() == 1:  # Laser not on sensor and button pressed
            warning("A robbery has been detected")
            robbery_activity(components)  # Execute the "there is a robbery function"
            return True  # Exit function with true
    except KeyError:  # This error will be call if the sensor is not calibrated
        warning("ThresholdSensitivity has not been calibrated")
    return False  # Exit function with false


def robbery_activity(components: dict):
    """
    This function will be executed when there is a robbery.
    """
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
