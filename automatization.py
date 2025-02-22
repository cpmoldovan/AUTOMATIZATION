#Automation of contracts
import sys
import cgi
import time
from docxtpl import DocxTemplate
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
from io import StringIO
import urllib
import html

HOST_NAME = "127.0.0.1"
PORT = 8080


def read_html_template(path):
    """function to read HTML file"""
    try:
        with open(path) as f:
            file = f.read()
    except Exception as e:
        file = e
    return file


class PythonServer(SimpleHTTPRequestHandler):
    """Python HTTP Server that handles GET and POST requests"""
    paths = ["/documente_create"]
    flag = 1
    def do_GET(self):
        if self.path == '/':
            self.path = './templates/index.html'
            file = read_html_template(self.path)
            self.send_response(200, "OK")
            self.end_headers()
            self.wfile.write(bytes(file, "utf-8"))

        if self.path == '/documente_create':
            self.send_response(200, "OK")
            self.end_headers()
            self.list_directory('documente_create')

    def list_directory(self, path):
        if self.flag == 0:
            try:
                list = os.listdir(path.decode("utf8"))
            except os.error:
                self.send_error(404, "No permission to list directory")
                return None
        else:
            try:
                list = self.paths
            except os.error:
                self.send_error(404, "No permission to list directory")
                return None
        list.sort(key=lambda a: a.lower())
        f = StringIO()
        displaypath = "Requested Files"
        f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
        f.write("<html>\n<title>Directory listing for %s</title>\n" % displaypath)
        f.write("<body>\n<h2>Directory listing for %s</h2>\n" % displaypath)
        f.write("<hr>\n<ul>\n")
        for dirname in list:
            name = os.path.basename(dirname)
            name = name.encode("utf8")
            fullname = dirname.encode('utf8')
            displayname = linkname = name
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
            if os.path.islink(fullname):
                displayname = name + "@"
                # Note: a link to a directory displays with @ and links with /
            
            f.write('<li><a href="%s">%s</a>\n'
                    % (urllib.parse.quote(fullname), urllib.parse.quote(fullname)))
        f.write("</ul>\n<hr>\n</body>\n</html>\n")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        encoding = "utf-8"
        self.send_header("Content-type", "text/html; charset=%s" % encoding)
        self.send_header("Content-Length", str(length))
        self.end_headers()
        return f

    def do_POST(self):
        if self.path == '/success':

            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')

            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)

                doc = DocxTemplate("./templates/template.docx")

                context = {
                "no_registration":fields.get("no_registration")[0],
                "date":fields.get("date")[0],
                "company_name":fields.get("company_name")[0],
                "administrator_name":fields.get("administrator_name")[0],
                "contract_value":fields.get("contract_value")[0],
                "price_include":fields.get("price_include")[0],
                "contract_duration":fields.get("contract_duration")[0],
                "advance_payment_percentage":fields.get("advance_payment_percentage")[0],
                "left_payment_percentage":fields.get("left_payment_percentage")[0],
                }

                doc.render(context)
                timestr = time.strftime("%d%m%Y-%H%M%S")
                nume_fisier = "./documente_create/contract-" + timestr + ".docx"
                doc.save(nume_fisier)

                self.send_response(200)
                self.send_header('Content-type', 'application/docx')
                self.send_header('Content-Disposition', 'attachment; filename="contract_' + fields.get("company_name")[0] + '.docx"')
                self.end_headers()
                with open(nume_fisier, 'rb') as file: 
                    self.wfile.write(file.read()) # Read the file and send the contents 

if __name__ == "__main__":
    server = HTTPServer((HOST_NAME, PORT), PythonServer)
    print(f"Server started http://{HOST_NAME}:{PORT}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        print("Server stopped successfully")
        sys.exit(0)