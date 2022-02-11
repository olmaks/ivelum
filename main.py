from http_handler import WebHandler, ThreadedHTTPServer


def perform_port_validation(port):
    error_msg = 'Incorrect port number'
    try:
        port = int(port)
    except ValueError:
        raise Exception(error_msg)
    if port not in range(1, 65536):
        raise Exception(error_msg)
    return port


if __name__ == '__main__':
    port = input('Please enter the free port number: ')
    validated_port = perform_port_validation(port)
    with ThreadedHTTPServer(("", validated_port), WebHandler) as httpd:
        print('Serving at port:', port, 'Use <Ctrl-C> to stop')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('Thanks for using!')
