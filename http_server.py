from os.path import isfile, join
from http.server import BaseHTTPRequestHandler, HTTPServer

SERVER_ADDR = "0.0.0.0"
SERVER_PORT = 80

SERVER_DIR = "http"

class HTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        file_path = join(SERVER_DIR, self.path.split("/")[-1])
        if(file_path == SERVER_DIR + "\\"):  #requesting the index page
            print("Sending index page")
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(open(file_path + "index.html", "rb").read())
        elif isfile(file_path):  #requesting another page
            print("Sending {}".format(file_path))
            self.send_response(200)
            file_name = file_path.split("\\")[-1]
            file_ext = file_name.split(".")[-1]
            content_type = None
            if file_ext == "html":
                content_type = "text/html"
            elif file_ext == "css":
                content_type = "text/css"
            elif file_ext == "js":
                content_type = "text/javascript"
            self.send_header('Content-Type', content_type)
            self.end_headers()
            self.wfile.write(open(file_path, "rb").read())
        else:
            print("Sending 404 for {}".format(file_path))
            self.send_response(404)
            self.end_headers()

with HTTPServer((SERVER_ADDR, SERVER_PORT), HTTPHandler) as httpd:
    print("Serving on port {}".format(SERVER_PORT))
    httpd.serve_forever()