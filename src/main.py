import log
import hardware
import networkManager
import miscellaneous as misc
import socket

log.message("Main.py start")


def main():
    log.message("Main function start")

    components = hardware.setup_components(misc.read_json("data/config")["components"])  # initialize all the components
    display_header = ""
    display_body = []

    #hardware.calibrateSensor(components)  # calibrate the sensor

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 80))
    s.listen(5)

    while True:
        try:
            connection_socket, address = s.accept()
            print('Got a connection from %s' % str(address))

            networkManager.network_handler(connection_socket, components)
        except OSError:
            log.debugging("Socket timeout")

        if components["button"]["object"].value() == 1:  # button pressed
            components["led"]["object"].on()
            components["laser"]["object"].on()
        else:
            components["led"]["object"].off()
            components["laser"]["object"].off()

        try:
            if components["lightSensor"]["object"].read() > components["lightSensor"]["thresholdSensitivity"] and \
                    components["button"]["object"].value() == 1:  # laser on sensor and button pressed
                log.repeat_message("Laser on light sensor", 10, "laser on light")
                alarm(components)
        except KeyError:
            log.warning("ThresholdSensitivity has not been calibrated")

    log.error("Main function stops")


def alarm(components):
    components["led"]["object"].on()
    components["motor"]["object"].forward(50)
    components["speaker"]["object"].alarm()
    from hardware import update_display
    update_display(components, "De dief is er")


if __name__ == '__main__':  # check if python is ready
    main()
else:
    log.error("Main failed")
