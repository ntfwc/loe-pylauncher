# Copyright (c) 2017 ntfwc
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import urllib.request
import http.client

CONTENT_LENGTH_HEADER = "content-length"

def downloadUrlContent(url, maxContentLength, timeout):
    """ Downloads the content of the given URL

    :param str url: An URL
    :param int maxContentLength: The max content length to allow 
    :param int or float timeout: The request timeout in seconds
    """
    response = urllib.request.urlopen(url, timeout=timeout)
    try:
        if response.code != http.client.OK:
            print("Debug[web_io.py]: '%s' Received non-OK Http response. code=%s" % (url, response.code))
            return None

        info = response.info()
        if not CONTENT_LENGTH_HEADER in info:
            print("Debug[web_io.py]: '%s' Received http response without a content-length header" % url)
            return None

        contentLength = int(info[CONTENT_LENGTH_HEADER])
        if contentLength > maxContentLength:
            print("Debug[web_io.py]: '%s' Received http response with a content-length longer than the max allowed. max=%d, content-length=%d" % (url, maxContentLength, contentLength))
            return None

        data = response.read(contentLength)
        if len(data) != contentLength:
            print("Debug[web_io.py]: '%s' Was not able to read the advertised content-length" % url)

        return data
    finally:
        response.close()

