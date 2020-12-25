def network_handler(socket, components: dict):
    from log import debugging
    request = socket.recv(1024)
    request = str(request)
    debugging('Socket content = {}'.format(request))

    motor_off = request.find('/?moveMotor=off')
    motor_left = request.find('/?moveMotor=left')
    motor_right = request.find('/?moveMotor=right')

    if motor_off == 6:
        debugging('Turn motor off')
        components["motor"]["object"].stop()
    elif motor_left == 6:
        debugging("Move motor left")
        components["motor"]["object"].forward(50)
    elif motor_right == 6:
        debugging("Move motor right")
        components["motor"]["object"].reverse(50)

    from miscellaneous import read_file
    """
    response = read_file("website/index.html")
    response = response.format(laser="whoo", senser="sensen", led="ledy")
    response = response.encode('utf-8')
    """
    socket.send('HTTP/1.1 200 OK\n'.encode('utf-8'))
    socket.send('Content-Type: text/html\n'.encode('utf-8'))
    socket.send('Connection: close\n\n'.encode('utf-8'))
    socket.sendall(read_file("website/index.html"))
    socket.close()
