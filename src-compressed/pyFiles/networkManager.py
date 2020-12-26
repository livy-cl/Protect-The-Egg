def network_handler(socket, components: dict, robbery_active: bool):
    from log import debugging, message
    request = str(socket.recv(1024))
    debugging('Socket content = {}'.format(request))
    if request.find('/?moveMotor=off') == 6:
        message('Turn motor off')
        components["motor"]["object"].stop()
    elif request.find(
            '/?moveMotor=left') == 6:
        message("Move motor left")
        components["motor"]["object"].forward(components["motor"]["speed"])
    elif request.find('/?moveMotor=right') == 6:
        message("Move motor right")
        components["motor"]["object"].reverse(components["motor"]["speed"])
    elif request.find('/?laserState=off') == 6:
        components["laser"]["object"].off()
    elif request.find('/?laserState=on') == 6:
        components["laser"]["object"].on()
    elif request.find('/?moveMotorSpeed=lower') == 6:
        components["motor"]["speed"] -= 10
    elif request.find('/?moveMotorSpeed=higher') == 6:
        components["motor"]["speed"] += 10
    if not robbery_active:
        from miscellaneous import read_file
        response = read_file("index.html").split("%%%%%%%")
        response.insert(4, str(components["led"]["object"].value()))
        response.insert(3, str(components["lightSensor"]["object"].read()))
        response.insert(2, str(components["laser"]["object"].value()))
        response.insert(1, str(components["motor"]["speed"]))
        response = ''.join(map(str, response))
    else:
        response = """<h1 style="border: none; border-radius: 4px; color: white; padding: 16px 40px; font-size: 30px; 
        margin: 2px; cursor: pointer; background-color: #c92204; text-align: center;">There is a robbery</h1>"""
    socket.send('HTTP/1.1 200 OK\n'.encode('utf-8'))
    socket.send('Content-Type: text/html\n'.encode('utf-8'))
    socket.send('Connection: close\n\n'.encode('utf-8'))
    socket.sendall(response.encode('utf-8'))
    socket.close()
