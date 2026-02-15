import argparse
import configparser
from datetime import datetime
import grp,pwd
from fnmatch import fnmatch
import hashlib
from math import ceil
import os
import re 
import sys
import zlib

class gitRepo(object):
    workTree=None
    gitDir=None
    conf=None
    def __init__(self,path,force=False):
        self.workTree=path
        self.gitDir=os.path.join(self.workTree,".git")
        if not (force or os.path.isdir(self.gitDir)):
            raise Exception("No git directory found")
        self.conf=configparser.ConfigParser()
        cf=repoFile(self,"config")
        if cf and os.path.exists(cf):
            self.conf.read([cf])
        elif not force:
            raise Exception("Config File missing")
        if not force:
            ver=int(self.conf.get("core","repoformatversion"))
            if ver!=0:
                raise Exception("Version not supported")
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

class GitBlob(gitObject):
    fmt=b'blob'

    def serialize(self):
        return self.blobdata

    def deserialize(self, data):
        self.blobdata = data
def repoPath(repo,*path):
    return os.path.join(repo.gitDir,*path)
def repoFile(repo,*path,mkdir=False):
    if repoDir(repo,*path[:-1],mkdir=mkdir):
        return repoPath(repo,*path)
def repoCreate(path):
    repo=gitRepo(path,force=True)
    if os.path.exists(repo.workTree):
        if not os.path.isdir(repo.workTree):
            raise Exception(f"{path} is not a Directory")
        if os.path.exists(repo.gitDir) and os.listdir(repo.gitDir):
            raise Exception(f"{path} is not a epmty")
    else:
        os.makedirs(repo.workTree)
    assert repoDir(repo,"branches",mkdir=True)
    assert repoDir(repo,"objects",mkdir=True)
    assert repoDir(repo,"refs","tags",mkdir=True)
    assert repoDir(repo,"refs","heads",mkdir=True)
    #.git/desc
    with open(repoFile(repo,"description"),"w") as f:
        f.write("Unamed Repo;Change this descrption file to make an repositry.\n")
    #.git/head
    with open(repoFile(repo,"HEAD"),"w") as f:
        f.write("ref: refs/head/master\n")
    #.git/config
    with open(repoFile(repo,"config"),"w") as f:
        config=repoDefaultConfig()
        config.write(f)
    
    return repo
def repoDefaultConfig():
    ret=configparser.ConfigParser()
    ret.add_section("core")
    ret.set("core","repoformatversion","0")
    ret.set("core","bare","false")
    return ret   
def repoFind(path=".",required=True):
    path=os.path.realpath(path)
    if os.path.isdir(os.path.join(path,".git")):
        return gitRepo(path)
    parentPath=os.path.realpath(os.path.join(path,".."))
    if parentPath==path:
        if required:
            raise Exception("No git found")
        else:
            return None
    return repoFind(parentPath,required=required)


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
                raise Exception(f"Unknown type {fmt.decode("ascii")}")
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
def repoDir(repo,*path,mkdir=False):
    path=repoPath(repo,*path)
    if os.path.exists(path):
        if os.path.isdir(path):
            return path
        else:
            raise Exception("Invalid Path")
    if mkdir:
        os.makedirs(path)
        return path
    else:
        return None



def cmdInit(args):
    repoCreate(args.path)
def cmdHashObject(args):
    repo = repoFind() if args.write else None

    with open(args.path, "rb") as f:
        data = f.read()

    sha = objectHash(data, fmt=args.type.encode(), repo=repo)
    print(sha)


def objectHash(data, fmt, repo=None):
    match fmt:
        case b'commit': obj = GitCommit(data)
        case b'tree':   obj = GitTree(data)
        case b'tag':    obj = GitTag(data)
        case b'blob':   obj = GitBlob(data)
        case _: raise Exception(f"Unknown type {fmt}!")

    return objectWrite(obj, repo)

def catFile(repo,obj,fmt):
    obj=objectRead(repo,objectFind(repo,obj,fmt=fmt))
    sys.stdout.buffer.write(obj.serialize())
def cmdCatFile(args):
    repo=repoFind()
    catFile(repo,args.object,fmt=args.type.encode())
def objectFind(repo,name,fmt=None,follow=True):
    return name

argParser = argparse.ArgumentParser(description="Idiotic content tracker")

# subcommands container
argSubParser = argParser.add_subparsers(dest="command")
argSubParser.required = True


# ---------- init ----------
init_parser = argSubParser.add_parser("init", help="Initialize new repo")
init_parser.add_argument(
    "path",
    metavar="dir",
    nargs="?",
    default=".",
    help="Where to create the repository"
)


# ---------- cat-file ----------
cat_parser = argSubParser.add_parser(
    "cat-file",
    help="Provide content of repository objects"
)

cat_parser.add_argument(
    "type",
    choices=["blob", "commit", "tag", "tree"],
    help="Specify the type"
)

cat_parser.add_argument(
    "object",
    help="The object to display"
)


# ---------- hash-object ----------
hash_parser = argSubParser.add_parser(
    "hash-object",
    help="Compute object ID and optionally creates a blob from a file"
)

hash_parser.add_argument(
    "-t",
    dest="type",
    choices=["blob", "commit", "tag", "tree"],
    default="blob",
    help="Specify the type"
)

hash_parser.add_argument(
    "-w",
    dest="write",
    action="store_true",
    help="Actually write the object into the database"
)

hash_parser.add_argument(
    "path",
    help="Read object from <file>"
)
def main(argv=sys.argv[1:]):
    args=argParser.parse_args(argv)
    try:

        match args.command:
            case "add"          : cmdAdd(args)
            case "cat-file"     : cmdCatFile(args)
            case "check-ignore" : cmdCheckIgnore(args)
            case "checkout"     : cmdCheckout(args)
            case "commit"       : cmdCommit(args)
            case "hash-object"  : cmdHashObject(args)
            case "init"         : cmdInit(args)
            case "log"          : cmdLog(args)
            case "ls-files"     : cmdLsFiles(args)
            case "ls-tree"      : cmdLsTree(args)
            case "rev-parse"    : cmdRevParse(args)
            case "rm"           : cmdRm(args)
            case "show-ref"     : cmdShowRef(args)
            case "status"       : cmdStatus(args)
            case "tag"          : cmdTag(args)
            case _              : print("Bad command.")
    except Exception as e:
        print(e)