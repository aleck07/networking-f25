def getFileType(path):
    import os
    root, ext = os.path.splitext(path)
    return ext

def getMimeType(ext):
    import mimetypes
    mimeType, encoding = mimetypes.guess_type("file" + ext)
    return mimeType

print(getFileType("/somepath/somefile.html"))
print(getMimeType(".html"))
print(getMimeType(".png"))
print(getMimeType(".pdf"))