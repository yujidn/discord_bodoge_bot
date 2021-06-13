import ssl
from http.server import HTTPServer, SimpleHTTPRequestHandler

CERTFILE = "./localhost.pem"


def image_server_run(port=443):
    print(f"image_server_run port:{port}")
    Handler = SimpleHTTPRequestHandler

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(CERTFILE)

    with HTTPServer(("", port), Handler) as httpd:
        print("serving at address", httpd.server_address, "using cert file", CERTFILE)
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
        httpd.serve_forever()
