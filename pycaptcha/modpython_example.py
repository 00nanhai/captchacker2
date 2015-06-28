#
# An example that presents CAPTCHA tests in a web environment
# and gives the user a chance to solve them.
#
# This example is for use with Apache using mod_python and its
# Publisher handler. For example, if your apache configuration
# included something like:
#
#   AddHandler python-program .py
#   PythonHandler mod_python.publisher
#
# You could place this script anywhere in your web space to see
# the demo.
#
# --Micah <micah@navi.cx>
#

from Captcha.Visual import Tests
import Captcha
from mod_python import apache


def _getFactory(req):
    return Captcha.PersistentFactory("/tmp/pycaptcha_%s" % req.interpreter)


def test(req, name=Tests.__all__[0]):
    """Show a newly generated CAPTCHA of the given class.
       Default is the first class name given in Tests.__all__
       """
    test = _getFactory(req).new(getattr(Tests, name))

    # Make a list of tests other than the one we're using
    others = []
    for t in Tests.__all__:
        if t != name:
            others.append('<li><a href="?name=%s">%s</a></li>' % (t,t))
    others = "\n".join(others)

    return """<html>
<head>
<title>PyCAPTCHA Example</title>
</head>
<body>
<h1>PyCAPTCHA Example (for mod_python)</h1>
<p>
  <b>%s</b>:
  %s
</p>

<p><img src="image?id=%s"/></p>
<p>
  <form action="solution" method="get">
    Enter the word shown:
    <input type="text" name="word"/>
    <input type="hidden" name="id" value="%s"/>
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
""" % (test.__class__.__name__, test.__doc__, test.id, test.id, others)


def image(req, id):
    """Generate an image for the CAPTCHA with the given ID string"""
    test = _getFactory(req).get(id)
    if not test:
        raise apache.SERVER_RETURN, apache.HTTP_NOT_FOUND
    req.content_type = "image/jpeg"
    test.render().save(req, "JPEG")
    return apache.OK


def solution(req, id, word):
    """Grade a CAPTCHA given a solution word"""
    test = _getFactory(req).get(id)
    if not test:
        raise apache.SERVER_RETURN, apache.HTTP_NOT_FOUND

    if not test.valid:
        # Invalid tests will always return False, to prevent
        # random trial-and-error attacks. This could be confusing to a user...
        result = "Test invalidated, try another test"
    elif test.testSolutions([word]):
        result = "Correct"
    else:
        result = "Incorrect"

    return """<html>
<head>
<title>PyCAPTCHA Example</title>
</head>
<body>
<h1>PyCAPTCHA Example</h1>
<h2>%s</h2>
<p><img src="image?id=%s"/></p>
<p><b>%s</b></p>
<p>You guessed: %s</p>
<p>Possible solutions: %s</p>
<p><a href="test">Try again</a></p>
</body>
</html>
""" % (test.__class__.__name__, test.id, result, word, ", ".join(test.solutions))

### The End ###
