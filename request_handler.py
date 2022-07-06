import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from views.entry_requests import get_all_entries, get_single_entry
from views.entry_requests import delete_entry, create_entry
from views.entry_requests import search_entries, update_entry
from views.mood_requests import get_all_moods, get_single_mood


# Here's a class. It inherits from another class.
# Think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
class HandleRequests(BaseHTTPRequestHandler):
    # This is a Docstring it should be at the beginning of all classes and functions
    # It gives a description of the class or function
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """
    def parse_url(self, path):
        """Used for the search bar function in the app"""
        path_params = path.split("/") # splits on / basically removing it, leaving two elements
        resource = path_params[1]  # index 0 is empty, so start w/ index 1

        # Check if there is a query string parameter
        if "?" in resource:       # ex:  /entries?q=learning

            param = resource.split("?")[1]   # split on ? into two elements: q and searchstring
            resource = resource.split("?")[0]   # index 0 is the q
            pair = param.split("=")           # split on equal: [ 'q', 'searchstring' ]
            key = pair[0]              # KEY is at index 0
            value = pair[1]            # VALUE is at index 1

            return ( resource, key, value )

        # No query string parameter
        else:
            id = None

            try:
                id = int(path_params[2]) # TRY to do this action (convert index two of
            except IndexError:           # path_params into INT) and if Python encounters
                pass                     # an "IndexError", ignore it and don't stop the program
            except ValueError:           # or if Python encounters a "ValueError",
                pass                     # ignore it and don't stop the program

            return (resource, id)

    def do_DELETE(self):
        """Handles the DELETE requests to server"""
        # Set an HTTP 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "entries":
            delete_entry(id)

        # Encode the new entry and send in response
        self.wfile.write("".encode())

    # A class FN
    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    # Method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        """Handles GET requests to the server"""
        # Set the response code to 'Ok' [HTTP 200]
        self._set_headers(200)

        response = ""            # initialize the 'response' variable
        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)
        # Response from parse_url() is a tuple containing two items
        if len(parsed) == 2:
            ( resource, id ) = parsed
            if resource == "entries":
                if id is not None:
                    response = f"{get_single_entry(id)}"
                else:
                    response = f"{get_all_entries()}"
            if resource == "moods":
                if id is not None:
                    response = f"{get_single_mood(id)}"
                else:
                    response = f"{get_all_moods()}"

        if len(parsed) == 3:
            ( resource, key, value ) = parsed
            if (key == 'q'):
                response = search_entries(value)      
                          
        self.wfile.write(f"{response}".encode())
        
    # Method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        """Handles POST requests to the server"""
        # Set response code to 'Created'
        self._set_headers(201)

        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new entry
        new_entry = None

        # Add a new animal to the list.
        if resource == "entries":
            new_entry = create_entry(post_body)

        # Encode the new animal and send in response to the client, in JSON format
        self.wfile.write(f"{new_entry}".encode())


    # Method on the class that overrides the parent's method.
    # It handles any PUT request.

    def do_PUT(self):
        """Handles PUT requests to the server"""
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        success = False

        if resource == "entries":
            success = update_entry(id, post_body)
        # rest of the elif's

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())


# This FN is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8085 using the HandleRequests class
    """
    host = ''
    port = 8085
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
