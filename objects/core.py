import os
import zlib
import hashlib
from repo.core import repoFile

class gitObject(object):
    def __init__(self,data=None):
        if data!=None:
            self.deserialize(data)
        else:
            self.init()
    
    def deserialize(self,data):
        raise Exception("Not implemented")
    def serialize(self,data):
        raise Exception("Not implemented")
    def init(self,data):
        pass

class GitCommit(gitObject):
    fmt=b'commit'

class GitTree(gitObject):
    fmt=b'tree'

class GitTag(gitObject):
    fmt=b'tag'

class GitBlob(gitObject):
    fmt=b'blob'

def objectRead(repo,sha):
    path=repoFile(repo,"objects",sha[0:2],sha[2:])
    if not os.path.isfile(path):
        return None
    with open(path,"rb") as f:
        raw=zlib.decompress(f.read())
        x=raw.find(b' ')
        fmt=raw[0:x]
        y=raw.find(b"\x00",x)
        size=int(raw[x:y].decode("ascii"))
        if size!=len(raw)-y-1:
            raise Exception(f"Malformed Object {sha}")
        match fmt:
            case b'commit' :c=GitCommit
            case b"tree" :c=GitTree
            case b"tag" :c=GitTag
            case b"blob" :c=GitBlob
            case _:
                raise Exception(f"Unknown type {fmt.decode('ascii')}")
        return c(raw[y+1:])

def objectWrite(obj,repo=None):
    data=obj.serialize()
    #Add Header
    res=obj.fmt+b" "+str(len(data)).encode()+b"\x00"+data
    sha=hashlib.sha1(res).hexdigest()
    if repo:
        path=repoFile(repo,"objects",sha[:2],sha[2:],mkdir=True)
        if not os.path.exists(path):
            with open(path,"wb") as f:
                f.write(zlib.compress(res))
    return sha
