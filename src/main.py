import log
import hardware
import networkManager
import miscellaneous as misc
import socket

log.message("Main.py start")


def main():
    log.message("Main function start")

    html = """<html><head> <title>ESP Web Server</title><meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
    h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
    border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
    .button2{background-color: #4286f4;}</style></head><body> <h1>ESP Web Server</h1> 
    <p>GPIO state: <strong>""" + "gpio_state" + """</strong></p><p><a href="/?led=on"><button class="button">ON</button></a></p>
    <p><a href="/?led=off"><button class="button button2">OFF</button></a></p></body></html>"""

    components = hardware.setup_components(misc.read_json("data/config")["components"])  # initialize all the components
    display_header = ""
    display_body = []

    # hardware.calibrateSensor(components)  # calibrate the sensor

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        request = str(request)
        print('Content = %s' % request)
        led_on = request.find('/?led=on')
        led_off = request.find('/?led=off')
        if led_on == 6:
            print('LED ON')
        if led_off == 6:
            print('LED OFF')
        response = html
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()

        """
        if components["button"]["object"].value() == 1:  # button pressed
            components["led"]["object"].on()
            components["laser"]["object"].on()
            components["motor"]["object"].forward(50)
        else:
            components["led"]["object"].off()
            components["laser"]["object"].off()
            components["motor"]["object"].stop()

        
        if components["lightSensor"]["object"].read() > components["lightSensor"]["thresholdSensitivity"] and \
                components["button"]["object"].value() == 1:  # laser on sensor and button pressed
            log.repeat_message("Laser on light sensor", 10, "laser on light")
        """

    log.error("Main function stops")


if __name__ == '__main__':  # check if python is ready
    main()
else:
    log.error("Main failed")
