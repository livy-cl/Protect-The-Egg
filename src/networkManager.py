def network_handler(socket, components: dict, robbery_active: bool):
    from log import debugging, message

    request = str(socket.recv(1024))  # save the request in a variable as string
    debugging('Socket content = {}'.format(request))

    if request.find('/?moveMotor=off') == 6:  # search if the variable request has the string "/?moveMotor=off"
        message('Turn motor off')
        components["motor"]["object"].stop()  # turn motor off
    elif request.find(
            '/?moveMotor=left') == 6:  # for this and all following if statements see the command on the first
        # if statement
        message("Move motor left")
        components["motor"]["object"].forward(components["motor"]["speed"])  # let motor go forward
    elif request.find('/?moveMotor=right') == 6:
        message("Move motor right")
        components["motor"]["object"].reverse(components["motor"]["speed"])  # let motor go in reverse
    elif request.find('/?laserState=off') == 6:
        components["laser"]["object"].off()  # turn laser off
    elif request.find('/?laserState=on') == 6:
        components["laser"]["object"].on()  # turn laser on
    elif request.find('/?moveMotorSpeed=lower') == 6:
        components["motor"]["speed"] -= 10  # add -10 to speed
    elif request.find('/?moveMotorSpeed=higher') == 6:
        components["motor"]["speed"] += 10  # add 10 to speed

    if not robbery_active:
        from miscellaneous import read_file
        response = read_file("index.html").split("%%%%%%%")  # split the code at "%%%%%%%" into a list
        response.insert(4, str(components["led"]["object"].value()))  # at index 4 add the led state
        response.insert(3, str(components["lightSensor"]["object"].read()))  # at index 3 add the light sensor value
        response.insert(2, str(components["laser"]["object"].value()))  # at index 2 add the laser state
        response.insert(1, str(components["motor"]["speed"]))  # at index 1 add the motor speed

        response = ''.join(map(str, response))  # add the list to one big string
    else:  # the html code when there is a robbery
        response = """<h1 style="border: none; border-radius: 4px; color: white; padding: 16px 40px; font-size: 30px; 
        margin: 2px; cursor: pointer; background-color: #c92204; text-align: center;">There is a robbery</h1>"""

    socket.send('HTTP/1.1 200 OK\n'.encode('utf-8'))
    socket.send('Content-Type: text/html\n'.encode('utf-8'))
    socket.send('Connection: close\n\n'.encode('utf-8'))
    socket.sendall(response.encode('utf-8'))  # encode and send the (encoded) string
    socket.close()
