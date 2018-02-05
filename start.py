import BaseHTTPServer
import orm_db
import cgi

class reqHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def sHeader(self):
        self.request_version = 'HTTP/1.1'
        self.send_header('content_type','text/html')
        self.end_headers()

    def do_GET(self):
        self.send_response(200,'OK')
        self.sHeader()
        query = self.path.split("/")

        if self.path == '/':
            self.wfile.write(orm_db.getData('menuitem'))
        elif self.path.startswith('/delete'):
            self.wfile.write(orm_db.delData(query[2],query[3]))
        elif self.path.startswith('/edit'):
            self.wfile.write(orm_db.getOneData(query[2],query[3]))
        else:
            self.wfile.write(orm_db.getData(query[1]))


    def do_POST(self):
        self.send_response(301)
        self.sHeader()
        query = self.path.split("/")

        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
            fields = cgi.parse_multipart(self.rfile, pdict)
            messagecontent = fields.get('message')
        if self.path.startswith('/edit'):
            self.wfile.write(orm_db.updateData(query[2],query[3],messagecontent[0]))
        elif self.path.startswith('/add'):
            self.wfile.write(orm_db.createData(query[2],messagecontent[0]))

if __name__ == '__main__':
    try:
        server_address = ('',8000)
        httpd = BaseHTTPServer.HTTPServer(server_address, reqHandler)
        print 'Server is running on 127.0.0.1:8000'
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.socket.close()
