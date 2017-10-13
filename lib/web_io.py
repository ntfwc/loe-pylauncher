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

