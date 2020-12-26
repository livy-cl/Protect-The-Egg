import machine as machine
def setup_components(component_dict: dict) -> dict:
    from ssd1306 import SSD1306_I2C
    from machine import Pin, ADC, I2C
    final_dict = {}
    for component_key, component_value in component_dict["normalSetup"].items():
        final_dict[component_key] = component_value
        final_dict[component_key]["object"] = Pin(component_value["pin"],Pin.IN if component_value["pinIn"] is True else Pin.OUT,Pin.PULL_UP if component_value["pullUp"] is True else None)
    for component_key, component_value in component_dict["specialSetup"].items():
        if component_value["type"] == "motor":
            final_dict[component_key] = component_value
            final_dict[component_key]["object"] = DS04NFC(Pin(final_dict[component_key]["pin"], Pin.OUT))
        elif component_value["type"] == "lightSensor":
            final_dict[component_key] = component_value
            final_dict[component_key]["object"] = ADC(final_dict[component_key]["pin"])
        elif component_value["type"] == "OLEDDisplay":
            final_dict[component_key] = component_value
            final_dict[component_key]["I2C"] = I2C(-1,scl=Pin(final_dict[component_key]["SCKPin"]),sda=Pin(final_dict[component_key]["SDAPin"]))
            final_dict[component_key]["object"] = SSD1306_I2C(final_dict[component_key]["width"],final_dict[component_key]["height"],final_dict[component_key]["I2C"])
        elif component_value["type"] == "speaker":
            final_dict[component_key] = component_value
            final_dict[component_key]["object"] = SpeakerController(final_dict[component_key]["pin"])
        else:
            from log import warning
            warning("Special component " + component_key + " has not been setup")
    return final_dict
class DS04NFC:
    def __init__(self, pin):
        from machine import PWM
        self.pwm = PWM(pin, freq=50)
        self.pwm.duty(75)
    def stop(self):
        self.pwm.duty(75)
    def forward(self, speed: int = 100):
        speed = int((((speed - 0) * (100 - 75)) / (100 - 0)) + 75)
        self.pwm.duty(speed)
    def reverse(self, speed: int = 100):
        speed = int((((speed - 0) * (50 - 75)) / (100 - 0)) + 75)
        self.pwm.duty(speed)
class SpeakerController:
    def __init__(self, pin):
        from machine import Pin, PWM
        self.pin = Pin(pin, Pin.OUT)
        self.pwm = PWM(self.pin)
        self.pwm.deinit()
        self.pin.on()
    def alarm(self, freq=500, duty=550):
        from machine import PWM
        self.pwm = PWM(self.pin)
        self.pwm.init(freq=freq, duty=duty)
    def stop(self):
        self.pwm.deinit()
def pulse_pwm(pwm: machine.PWM, time: int):
    from utime import sleep_ms
    from math import sin, pi
    for index in range(20):
        pwm.duty(int(sin(index / 10 * pi) * 500 + 500))
        sleep_ms(time)
def calibrate_sensor(components: dict):
    from utime import sleep
    from log import message, warning, debugging
    message("Start calibrating")
    update_display(components, "calibrate sensor", ["Do not shine any","light on the","sensor. Then","press the button."])
    while True:
        if components["button"]["object"].value() == 1:
            break
        elif components["configButton"]["object"].value() == 1:
            warning("Stopped calibrating sensor")
            update_display(components)
            return
    components["lightSensor"]["normalSensitivity"] = components["lightSensor"]["object"].read()
    debugging("Normal sensitivity: " + str(components["lightSensor"]["normalSensitivity"]))
    update_display(components, "calibrate sensor", ["Shine the laser","on the sensor.","Then press the","button."])
    components["laser"]["object"].on()
    sleep(3)
    while True:
        if components["button"]["object"].value() == 1:
            break
        elif components["configButton"]["object"].value() == 1:
            warning("Stopped calibrating sensor")
            update_display(components)
            return
    components["lightSensor"]["laserSensitivity"] = components["lightSensor"]["object"].read()
    debugging("Laser sensitivity: " + str(components["lightSensor"]["laserSensitivity"]))
    update_display(components)
    components["laser"]["object"].off()
    threshold_sensitivity_offset = 100
    components["lightSensor"]["thresholdSensitivity"] = int((components["lightSensor"]["laserSensitivity"] +components["lightSensor"]["normalSensitivity"])/2+threshold_sensitivity_offset)
    debugging("Threshold sensitivity: " + str(components["lightSensor"]["thresholdSensitivity"]))
    message("Calibrating done")
def update_display(components, header: str = None, body: list = None):
    from miscellaneous import read_json, write_json
    json_dict = read_json("data/dump")
    if not header == json_dict["display"]["header"] or not body == json_dict["display"]["body"]:
        json_dict["display"]["header"] = header
        json_dict["display"]["body"] = body
        components["OLEDDisplay"]["object"].fill(0)
        if header is not None:
            components["OLEDDisplay"]["object"].text(str(header), 0, 5)
        if body is not None:
            for index, value in enumerate(body):
                if not value == "":
                    components["OLEDDisplay"]["object"].text(str(value), 0, ((index + 1) * 10) + 10)
        components["OLEDDisplay"]["object"].show()
        write_json("data/dump", json_dict)
        from log import debugging
        debugging("Updated display")
        return True