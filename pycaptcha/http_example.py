#!/usr/bin/env python
#
# An example that presents CAPTCHA tests in a web environment
# and gives the user a chance to solve them. Run it, optionally
# specifying a port number on the command line, then point your web
# browser at the given URL.
#

from Captcha.Visual import Tests
from Captcha import Factory
import BaseHTTPServer, urlparse, sys


class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        scheme, host, path, parameters, query, fragment = urlparse.urlparse(self.path)

        # Split the path into segments
        pathSegments = path.split('/')[1:]

        # Split the query into key-value pairs
        args = {}
        for pair in query.split("&"):
            if pair.find("=") >= 0:
                key, value = pair.split("=", 1)
                args.setdefault(key, []).append(value)
            else:
                args[pair] = []

        # A hack so it works with a proxy configured for VHostMonster :)
        if pathSegments[0] == "vhost":
            pathSegments = pathSegments[3:]

        if pathSegments[0] == "":
            self.handleRootPage(args.get('test', Tests.__all__)[0])

        elif pathSegments[0] == "images":
            self.handleImagePage(pathSegments[1])

        elif pathSegments[0] == "solutions":
            self.handleSolutionPage(pathSegments[1], args['word'][0])

        else:
            self.handle404()

    def handle404(self):
        self.send_response(404)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write("<html><body><h1>No such resource</h1></body></html>")

    def handleRootPage(self, testName):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()

        test = self.captchaFactory.new(getattr(Tests, testName))

        # Make a list of tests other than the one we're using
        others = []
        for t in Tests.__all__:
            if t != testName:
                others.append('<li><a href="/?test=%s">%s</a></li>' % (t,t))
        others = "\n".join(others)

        self.wfile.write("""<html>
<head>
<title>PyCAPTCHA Example</title>
</head>
<body>
<h1>PyCAPTCHA Example</h1>
<p>
  <b>%s</b>:
  %s
</p>

<p><img src="/images/%s"/></p>
<p>
  <form action="/solutions/%s" method="get">
    Enter the word shown:
    <input type="text" name="word"/>
  </form>
</p>

<p>
Or try...
<ul>
%s
</ul>
</p>

</body>
</html>
""" % (test.__class__.__name__, test.__doc__, test.id, test.id, others))

    def handleImagePage(self, id):
        test = self.captchaFactory.get(id)
        if not test:
            return self.handle404()

        self.send_response(200)
        self.send_header("Content-Type", "image/jpeg")
        self.end_headers()
        test.render().save(self.wfile, "JPEG")

    def handleSolutionPage(self, id, word):
        test = self.captchaFactory.get(id)
        if not test:
            return self.handle404()

        if not test.valid:
            # Invalid tests will always return False, to prevent
            # random trial-and-error attacks. This could be confusing to a user...
            result = "Test invalidated, try another test"
        elif test.testSolutions([word]):
            result = "Correct"
        else:
            result = "Incorrect"

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write("""<html>
<head>
<title>PyCAPTCHA Example</title>
</head>
<body>
<h1>PyCAPTCHA Example</h1>
<h2>%s</h2>
<p><img src="/images/%s"/></p>
<p><b>%s</b></p>
<p>You guessed: %s</p>
<p>Possible solutions: %s</p>
<p><a href="/">Try again</a></p>
</body>
</html>
""" % (test.__class__.__name__, test.id, result, word, ", ".join(test.solutions)))


def main(port):
    print "Starting server at http://localhost:%d/" % port
    handler = RequestHandler
    handler.captchaFactory = Factory()
    BaseHTTPServer.HTTPServer(('', port), RequestHandler).serve_forever()

if __name__ == "__main__":
    # The port number can be specified on the command line, default is 8080
    if len(sys.argv) >= 2:
        port = int(sys.argv[1])
    else:
        port = 8080
    main(port)

### The End ###
