import machine
import log


def setup_components(component_dict: dict) -> dict:
    """
    create object for all the components in the given dictionary

    :param component_dict: the dictionary with all the components
    :return: the dictionary with the components and the object for the components
    """
    from ssd1306 import SSD1306_I2C
    final_dict = {}

    # normal setup
    for component_key, component_value in component_dict["normalSetup"].items():  # loop through the normal components
        final_dict[component_key] = component_value  # save component to return dictionary
        final_dict[component_key]["object"] = machine.Pin(  # make component machine.Pin class
            component_value["pin"],  # give pin parameter
            machine.Pin.IN if component_value["pinIn"] is True else machine.Pin.OUT,  # check if component is output
            # or input
            machine.Pin.PULL_UP if component_value["pullUp"] is True else None)  # check if you need a PULL_UP resistor

    for component_key, component_value in component_dict["specialSetup"].items():  # loop through the special components
        if component_value["type"] == "motor":  # motor component
            final_dict[component_key] = component_value  # save component to return dictionary
            final_dict[component_key]["object"] = DS04NFC(machine.Pin(final_dict[component_key]["pin"],  # motor class
                                                                      machine.Pin.OUT))
        elif component_value["type"] == "lightSensor":  # light sensor component
            final_dict[component_key] = component_value  # save component to return dictionary
            final_dict[component_key]["object"] = machine.ADC(final_dict[component_key]["pin"])  # analog to digital
            # class

        elif component_value["type"] == "OLEDDisplay":  # OLED display component
            final_dict[component_key] = component_value  # save component to return dictionary
            final_dict[component_key]["I2C"] = machine.I2C(-1,  # I2C protocol class
                                                           scl=machine.Pin(final_dict[component_key]["SCKPin"]),
                                                           sda=machine.Pin(final_dict[component_key]["SDAPin"]))
            final_dict[component_key]["object"] = SSD1306_I2C(final_dict[component_key]["width"],  # display class
                                                              final_dict[component_key]["height"],
                                                              final_dict[component_key]["I2C"])

        elif component_value["type"] == "speaker":  # speaker component
            final_dict[component_key] = component_value
            final_dict[component_key]["object"] = SpeakerController(final_dict[component_key]["pin"])

        else:  # any left over/ net programmed components
            log.warning("Special component " + component_key + " has not been setup")

    return final_dict


class DS04NFC:
    def __init__(self, pin):
        """
        a class for the DS04-NFC motor

        :param pin: the pin of the DS04-NFC motor
        """
        self.pwm = machine.PWM(pin, freq=50)
        self.pwm.duty(75)

    def stop(self):
        """
        issue stop impulse to stop the motor
        """
        self.pwm.duty(75)

    def forward(self, speed: int = 100):
        """
        issue forward impulse to start the motor

        :param speed: the speed of the motor turning
        """

        # map number in range to another range: (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
        speed = int((((speed - 0) * (100 - 75)) / (100 - 0)) + 75)
        self.pwm.duty(speed)

    def reverse(self, speed: int = 100):
        """
        issue reverse impulse to start the motor

        :param speed: the speed of the motor turning
        """

        # map number in range to another range: (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
        speed = int((((speed - 0) * (50 - 75)) / (100 - 0)) + 75)
        self.pwm.duty(speed)


class SpeakerController:
    def __init__(self, pin):
        """
        Controller for the speaker

        :param pin: the bin of the low voltage audio amplifier
        """
        self.pin = machine.Pin(pin, machine.Pin.OUT)
        self.pwm = machine.PWM(self.pin)
        self.pwm.deinit()
        self.pin.on()

    def alarm(self, freq=500, duty=550):
        """
        Makes a pwm. This pwm gives a signal to the audio amplifier who then amplifies the pwm to the speaker
        :param freq: frequency of the pwm
        :param duty: the duty of the pwm
        """
        self.pwm = machine.PWM(self.pin)
        self.pwm.init(freq=freq, duty=duty)

    def stop(self):
        """
        Stops/deinits the pwm
        """
        try:
            self.pwm.deinit()
        except:
            log.debugging("There is no pwm object in speaker controller class")


def pulse_pwm(pwm: machine.PWM, time: int):
    """
    pulse a pin with pwm

    :param pwm: pulse width modulation object
    :param time: time to pulse pwm
    """
    from utime import sleep_ms
    from math import sin, pi

    for index in range(20):
        pwm.duty(int(sin(index / 10 * pi) * 500 + 500))
        sleep_ms(time)


def calibrateSensor(components: dict):
    """
    gets the sensor state without light and with light then calculates the middle of the 2 values

    :param components: the dictionary of al the components (that is calculated at hardware.setup_pins())
    """
    from utime import sleep

    log.message("Start calibrating")

    update_display(components, "calibrate sensor", ["Do not shine any",  # display text
                                                    "light on the",
                                                    "sensor. Then",
                                                    "press the button."])

    while True:  # wait for the button to be pressed
        if components["button"]["object"].value() == 1:
            break

    components["lightSensor"]["normalSensitivity"] = components["lightSensor"]["object"].read()  # save sensor value
    log.debugging("Normal sensitivity: " + str(components["lightSensor"]["normalSensitivity"]))  # print sensor value

    update_display(components, "calibrate sensor", ["Shine the laser",  # display text
                                                    "on the sensor.",
                                                    "Then press the",
                                                    "button."])

    components["laser"]["object"].on()  # turn laser on
    sleep(3)

    while True:  # wait for the button to be pressed
        if components["button"]["object"].value() == 1:
            break

    components["lightSensor"]["laserSensitivity"] = components["lightSensor"]["object"].read()  # save sensor value
    log.debugging("Laser sensitivity: " + str(components["lightSensor"]["laserSensitivity"]))  # print sensor value

    update_display(components)  # clear display
    components["laser"]["object"].off()  # turn laser off

    # calculate middle of normal sensitivity and laser sensitivity then add an offset
    threshold_sensitivity_offset = 100
    components["lightSensor"]["thresholdSensitivity"] = int((components["lightSensor"]["laserSensitivity"] +
                                                             components["lightSensor"]["normalSensitivity"]) / 2 +
                                                            threshold_sensitivity_offset)

    log.debugging("Threshold sensitivity: " + str(components["lightSensor"]["thresholdSensitivity"]))  # print threshold
    log.message("Calibrating done")


def update_display(components, header: str = None, body: list = None):
    """
    updates the display if there is a change in the body and header compared to the previous time

    :param components: the dictionary with al the components
    :param header: the top line of the display (the yellow part of the display)
    :param body: the main part of the display from line +-20 to +-50 (the blue part of the display)
    :return: returns True if the display updated
    """
    from miscellaneous import read_json, write_json

    json_dict = read_json("data/dump")
    if not header == json_dict["display"]["header"] or not body == json_dict["display"]["body"]:  # check if body and/or
        # header has chanced

        json_dict["display"]["header"] = header  # add header to json dictionary
        json_dict["display"]["body"] = body  # add body to json dictionary

        components["OLEDDisplay"]["object"].fill(0)  # clear display

        if header is not None:  # check if there is a header
            components["OLEDDisplay"]["object"].text(str(header), 0, 5)  # display header

        if body is not None:  # check if there is a body
            for index, value in enumerate(body):  # loop trough body
                if not value == "":  # check if there is text in this line of the body
                    components["OLEDDisplay"]["object"].text(str(value), 0, ((index + 1) * 10) + 10)  # display body

        components["OLEDDisplay"]["object"].show()  # update display

        write_json("data/dump", json_dict)  # write the body and header to the json file named dump

        log.debugging("Updated display")

        return True
