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



argParser=argparse.ArgumentParser(description="Idiotic content tracker")
argSubParser=argParser.add_subparsers(title="Command",dest="command")
argSubParser.required=True
argsp=argSubParser.add_parser("init",help="Intialize new repo")
argsp.add_argument("path",metavar="dir",nargs="?",default=".",help="Create new repo")

def cmdInit(args):
    repoCreate(args.path)
def main(argv=sys.argv[1:]):
    args=argParser.parse_args(argv)
    match args.command:
        case "add"          : cmd_add(args)
        case "cat-file"     : cmd_cat_file(args)
        case "check-ignore" : cmd_check_ignore(args)
        case "checkout"     : cmd_checkout(args)
        case "commit"       : cmd_commit(args)
        case "hash-object"  : cmd_hash_object(args)
        case "init"         : cmdInit(args)
        case "log"          : cmd_log(args)
        case "ls-files"     : cmd_ls_files(args)
        case "ls-tree"      : cmd_ls_tree(args)
        case "rev-parse"    : cmd_rev_parse(args)
        case "rm"           : cmd_rm(args)
        case "show-ref"     : cmd_show_ref(args)
        case "status"       : cmd_status(args)
        case "tag"          : cmd_tag(args)
        case _              : print("Bad command.")
        