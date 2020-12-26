import log
import hardware
import networkManager
import miscellaneous as misc
import socket

log.message("Main.py start")


def main():
    log.message("Main function start")

    components = hardware.setup_components(misc.read_json("data/config")["components"])  # initialize all the components
    robbery_active = False

    # hardware.calibrateSensor(components)  # calibrate the sensor

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 80))
    s.listen(5)

    while True:
        try:
            connection_socket, address = s.accept()
            print('Got a connection from %s' % str(address))

            networkManager.network_handler(connection_socket, components, robbery_active)
        except OSError:
            log.debugging("Socket timeout")

        if not robbery_active:
            robbery_active = normal_activity(components)


def normal_activity(components):
    if components["button"]["object"].value() == 1:  # button pressed
        if components["led"]["object"].value() == 0:  # check if led is off (so it does not turn it on when it is on)
            components["led"]["object"].on()  # turn led on
            log.debugging("Turn led on")
        if components["laser"]["object"].value() == 0:  # check if laser is off
            components["laser"]["object"].on()  # turn laser on
            log.warning("Turn laser on")
    else:
        if components["led"]["object"].value() == 1:  # check if led is on
            components["led"]["object"].off()  # turn led off
            log.debugging("Turn led off")
        if components["laser"]["object"].value() == 1:  # check if laser is on
            components["laser"]["object"].off()  # turn laser on
            log.warning("Turn laser off")
    try:
        if components["lightSensor"]["object"].read() > components["lightSensor"]["thresholdSensitivity"] and \
                components["button"]["object"].value() == 1:  # laser on sensor and button pressed
            log.repeat_message("Laser on light sensor", 10, "laser on light")
        else:
            log.warning("A robbery has been detected")
            robbery_activity(components)
            return True
    except KeyError:
        log.warning("ThresholdSensitivity has not been calibrated")
    return False


def robbery_activity(components):
    motor_speed = 50

    components["led"]["object"].on()
    components["motor"]["object"].forward(motor_speed)
    components["speaker"]["object"].alarm()
    from hardware import update_display
    update_display(components, "There is a robbery!!")


if __name__ == '__main__':  # check if python is ready
    main()
else:
    log.error("Main failed")
