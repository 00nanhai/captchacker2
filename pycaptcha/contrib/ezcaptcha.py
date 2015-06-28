#!/usr/bin/env python
"""
A simple module for delivering one-shot CAPTCHA challenges and processing
user responses, suited for web site usage.

Run this script as a CGI to see a simple demo in action (refer to
the function _demo() below).

Requirements:
    - python 2.2 or later
    - PyCAPTCHA (http://svn.navi.cx/misc/trunk/pycaptcha/)
    - PIL (http://www.pythonware.com/products/pil/)

Offers moderate security, since each CAPTCHA challenge has a timeout
attached to it, and can only be successfully answered once.

Follow these steps to perform a captcha cycle on your website:

    1. call getChallenge() to get a 'challenge key' string

    2. serve up a web form, containing:
        
        - this challenge key string as a hidden field
        - an image tag, for display of the challenge image
        - a normal text input field
       
       for example (assume the challenge key is 'yadayada')::
           
           <form method="POST" action="/index.cgi">
             ...
             <input type="hidden" name="captchaKey" value="yadayada"/>
             ...
             <img src="/index.cgi?cmd=getCaptchaImg&key=yadayada"/>
             <br/>
             ...
             Please type in the word from the image above:<br/>
             <input type="text" name="captcharesponse"/>
             ...
             <input type="submit" value="Submit"/>
             ...
           </form>

    3. When the client requests the challenge image (as caused by
       the <img> tag above):
        - get the key from the query string
        - call getImageData(key) to retrieve the image binary data
        - send this binary data back to the client with
          "Content-Type: image/jpeg"

    4. when the user posts back the form:
        - extract the user's answer and the key from the POSTed fields
        - call testSolution() with these values to see if the user has
          successfully read the word from the image, and done so within
          the timeout period

This module written by David McNab <david@rebirthing.co.nz>
"""
# ------------------------------------------------
# configuration items - set these here, or set them
# as module attributes when you import the module

# replace with your own gibberish
captchaSecretKey = "fR9^%tvHh2[+0_fxxhv$d(*rf!f$vns"

# timeout for the user to reply to the challenge
captchaTimeout = 3600

# ------------------------------------------------

import sys, os, StringIO, sha, base64, traceback
import random, time, tempfile

from Captcha.Visual.Tests import PseudoGimpy

# seed the prng

random.seed(time.time())

tmpdir = tempfile.gettempdir()

def getChallenge():
    """
    Returns a string, which should be placed as a hidden field
    on a web form. This string identifies a particular challenge,
    and is needed later for:
        - retrieving the image file for viewing the challenge, via
          call to getImageData()
        - testing a response to the challenge, via call to testSolution()

    The format of the string is::
        
        base64(id+":"+expirytime+":"+sha1(id, answer, expirytime, secret))
    
    Where:
        - id is a pseudo-random id identifying this challenge instance, and
          used to locate the temporary file under which the image is stored
        - expirytime is unixtime in hex
        - answer is the plaintext string of the word on the challenge picture
        - secret is the secret signing key 'captchaSecretKey
    """
    # get a CAPTCHA object
    g = PseudoGimpy()

    # retrieve text solution
    answer = g.solutions[0]
    
    # generate a unique id under which to save it
    id = _generateId(answer)

    # save the image to disk, so it can be delivered from the
    # browser's next request
    i = g.render()
    path = _getImagePath(id)
    f = file(path, "wb")
    i.save(f, "jpeg")
    f.close()

    # compute 'key'
    key = _encodeKey(id, answer)
    return key

def getImageData(key):
    id, expiry, sig = _decodeKey(key)
    return file(_getImagePath(id), "rb").read()

def testSolution(key, guess):
    """
    Tests if guess is a correct solution
    """
    try:
        id, expiry, sig = _decodeKey(key)

        # test for timeout
        if time.time() > expiry:
            # sorry, timed out, too late
            _delImage(id)
            return False

        # test for past usage of this key

        path = _getImagePath(id)
        if not os.path.isfile(path):
            # no such key, fail out
            return False

        # test for correct word
        if _signChallenge(id, guess, expiry) != sig:
            # sorry, wrong word
            return False

        # successful
        _delImage(id) # image no longer needed
        return True
    except:
        #traceback.print_exc()
        return False

# ----------------------------------------------------
# lower level funcs

def _encodeKey(id, answer):
    """
    Encodes the challenge ID and the answer into a string which is safe
    to give to a potentially hostile client

    The key is base64-encoding of 'id:expirytime:answer'
    """
    expiryTime = int(time.time() + captchaTimeout)
    sig = _signChallenge(id, answer, expiryTime)
    raw = "%s:%x:%s" % (id, expiryTime, sig)
    key = base64.encodestring(raw).replace("\n", "")
    return key

def _decodeKey(key):
    """
    decodes a given key, returns id, expiry time and signature
    """
    raw = base64.decodestring(key)
    id, expiry, sig = raw.split(":", 2)
    expiry = int(expiry, 16)
    return id, expiry, sig

def _signChallenge(id, answer, expiry):
    expiry = "%x" % expiry
    return sha.new(id + answer + expiry + captchaSecretKey).hexdigest()[:16]

def _generateId(solution):
    """
    returns a pseudo-random id under which picture
    gets stored
    """
    return sha.new(
        "%s%s%s" % (
            captchaSecretKey, solution, random.random())).hexdigest()[:10]

def _getImagePath(id):
    return os.path.join(tmpdir, id) + ".jpeg"

def _delImage(id):
    """
    deletes image from tmp dir, no longer wanted
    """
    try:
        imgPath = _getImagePath(id)
        if os.path.isfile(imgPath):
            os.unlink(imgPath)
    except:
        traceback.print_exc()
        pass



def _demo():
    """
    Presents a demo of this captcha module.
    
    If you run this file as a CGI in your web server, you'll see the demo
    in action
    """
    import cgi
    fields = cgi.FieldStorage()
    cmd = fields.getvalue("cmd", "")
    
    if not cmd:
        # first view
        key = getChallenge()
        print """Content-Type: text/html

<html>
 <head>
  <title>ezcaptcha demo</title>
 <head>
 <body>
  <h1>ezcaptcha demo</h1>
  <form method="POST">
   <input type="hidden" name="cmd" value="answerCaptcha">
   <input type="hidden" name="captchaKey" value="%s">
   <img src="?cmd=showCaptchaImg&captchaKey=%s">
   <br>
   Please type in the word you see in the image above:<br>
   <input type="text" name="captchaAnswer"><br>
   <input type="submit" value="Submit">
  </form>
 </body>
</html>
""" % (key, key)

    elif cmd == 'showCaptchaImg':
        # answer browser request for the CAPTCHA challenge image
        key = fields.getvalue("captchaKey")
        bindata = getImageData(key)
        print "Content-Type: image/jpeg"
        print
        print bindata

    elif cmd == 'answerCaptcha':
        # user has posted in an answer
        key = fields.getvalue("captchaKey")
        guess = fields.getvalue("captchaAnswer")
        
        # test user's answer
        if testSolution(key, guess) == True:
            # successful
            print """Content-Type: text/html

<html>
 <head>
  <title>ezcaptcha demo</title>
 </head>
 <body>
  <h1>ezcaptcha demo</h1>
  Successful!<br>
  <br>
  <a href="">Click here</a> for another demo
 </body>
</html>
"""

        else:
            # failed
            print """Content-Type: text/html

<html>
 <head>
  <title>ezcaptcha demo</title>
 <head>
 <body>
  <h1>ezcaptcha demo</h1>
  Sorry - that was wrong!
  <form method="POST">
   <input type="hidden" name="cmd" value="answerCaptcha">
   <input type="hidden" name="captchaKey" value="%s">
   <img src="?cmd=showCaptchaImg&captchaKey=%s">
   <br>
   Please type in the word you see in the image above:<br>
   <input type="text" name="captchaAnswer"><br>
   <input type="submit" value="Submit">
  </form>
 </body>
</html>
""" % (key, key)

if __name__ == '__main__':
    _demo()



