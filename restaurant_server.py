#/usr/env/python3

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
try:
    from urllib.parse import quote #python 3
except ImportError:
    from urllib import quote

# import CRUD Operations from Lesson 1
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # start prepping the HTML document regardless
        output = ""
        output += "<html><body>"
        closeout = "</body></html>"
        try:
            if self.path.endswith("/restaurants"):
                # Get the restaurant names
                restaurants = session.query(Restaurant).all()
                # headers
                output += "<a href =/new>Add a new restaurant here</a>"
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output += "<center><h1>Restaurants available in your city</h1></center>"
                output += "<br><br/><ul>"
                for restaurant in restaurants:
                    output += "<li>%s" % restaurant.name
                    output += '''<br><a href={0}/edit>Edit<a/><br>
                      <a href={0}/delete>Delete</a></li>'''.format(restaurant.id)
                output += closeout
            if self.path.endswith("/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output += '''<form
                  method='POST' enctype='multipart/form-data' action='/new'>
                  <h2>Name the Restaurant you would like to add</h2>
                  <input name="restaurant" type="text" >
                  <input type="submit" value="Submit">
                  </form>'''
                output += closeout
            if self.path.endswith("/edit"):
                output += "<CENTER><h1>WE'RE WORKING ON IT DAMMIT</H1></CENTER>"
                path_arr = self.path[1:].split("/")
                restaurant = session.query(Restaurant).filter(Restaurant.id == path_arr[0]).all()[0].__dict__
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output += '''<br><br>Edit name of Restaurant ID {0}, currently named {1}.
                  <br><form
                  method='POST' enctype='multipart/form-data' action='/{0}/edit'>
                  <br>
                  <input name="restaurant" type="text" >
                  <input type="hidden" name="restaurant_id" value="{0}">
                  <input type="submit" value="Submit">
                  </form>'''.format(restaurant['id'], restaurant['name'])
            if self.path.endswith("/delete"):
                output += "<CENTER><h1>WE'RE WORKING ON IT DAMMIT</H1></CENTER>"
                path_arr = self.path[1:].split("/")
                restaurant = session.query(Restaurant).filter(Restaurant.id == path_arr[0]).all()[0].__dict__
                output += """<form
                  method='POST' enctype='multipart/form-data'
                  action='/{0}/delete'>
                  <label for="delete">
                    Really delete Restaurant {0}?
                  </label>
                  <input id="delete" type="submit" value="Delete!">
                  </form>""".format(restaurant['id'], restaurant['name'])
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
            self.wfile.write(output)
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        print("Entered do_POST")
        try:
            print("This is trying my patience")
            print(self.path)
            print(self.path.endswith("/edit"))
            if self.path.endswith("/edit"):
                print("Editing...")
                ctype, pdict = cgi.parse_header(self.headers.getheader('Content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    new_name = fields.get('restaurant')
                    working_id = restaurantIDPath = self.path[1:].split("/")[0]
                    print(working_id)
                    to_update = (session.query(Restaurant).
                      filter_by(id=working_id).one())
                    if to_update != []:
                        to_update.name = new_name[0]
                        session.add(to_update)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()
                    else:
                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        output += """<center><h2>ID not recognized. Go
                          back to the beginning but we ain't giving you
                          a link."""
            if self.path.endswith("/delete"):
                print("Deleting...")
                ctype, pdict\
                  = cgi.parse_header(self.headers.getheader('Content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    new_name = fields.get('restaurant')
                    working_id = restaurantIDPath = self.path[1:].split("/")[0]
                    print(working_id)
                    session.query(Restaurant).filter(Restaurant.id
                      == working_id).delete(synchronize_session = False)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
            if self.path.endswith("/new"):
                print("nuuuuuu")
                ctype, pdict \
                  = cgi.parse_header(self.headers.getheader('Content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    form_content = fields.get('restaurant')
                    session.add(Restaurant(name = form_content[0]))
                    session.commit()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
        except Exception as e:
            print("DOINK!")
            print("Error e: {0}".format(e))

        @property
        def serialize(self):
            return {
                'id' : self.id,
                'name' : self.name,
                'course' : self.course
                'description' : self.description
                'price' : self.price
            }
def main():
    try:
        port = 8000
        server = HTTPServer(('', port), webServerHandler)
        print("Server running on port %s" % port)
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n Ctrl C entered, attempting to shut down server gracefully...")
        server.socket.close()

if __name__ == '__main__':
    main()
