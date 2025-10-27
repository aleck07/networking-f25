def getPathFromUrl(url):
    import urllib.parse
    parsedUrl = urllib.parse.urlparse(url)
    return parsedUrl.path

print(getPathFromUrl("http://www.example.com/somepath.html"))