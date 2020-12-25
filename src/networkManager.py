def network_handler(socket, components: dict):
    from log import debugging, message
    request = socket.recv(1024)
    request = str(request)
    debugging('Socket content = {}'.format(request))

    motor_off = request.find('/?moveMotor=off')
    motor_left = request.find('/?moveMotor=left')
    motor_right = request.find('/?moveMotor=right')

    if motor_off == 6:
        message('Turn motor off')
        components["motor"]["object"].stop()
    elif motor_left == 6:
        message("Move motor left")
        components["motor"]["object"].forward(50)
    elif motor_right == 6:
        message("Move motor right")
        components["motor"]["object"].reverse(50)

    from miscellaneous import read_file
    response = read_file("index.html").split("%%%%%%%")
    response.insert(3, str(components["led"]["object"].value()))
    response.insert(2, str(components["lightSensor"]["object"].read()))
    response.insert(1, str(components["laser"]["object"].value()))
    response = ''.join(map(str, response))
    response = response.encode('utf-8')

    socket.send('HTTP/1.1 200 OK\n'.encode('utf-8'))
    socket.send('Content-Type: text/html\n'.encode('utf-8'))
    socket.send('Connection: close\n\n'.encode('utf-8'))
    socket.sendall(response)
    socket.close()
