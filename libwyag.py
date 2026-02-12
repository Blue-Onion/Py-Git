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


argParser=argparse.ArgumentParser(description="Idiotic content tracker")
argSubParser=argParser.add_subparsers(title="Command",dest="command")
argSubParser.required=True
argSubParser.add_parser("add")
argSubParser.add_parser("cat-file")
argSubParser.add_parser("check-ignore")
argSubParser.add_parser("checkout")
argSubParser.add_parser("commit")
argSubParser.add_parser("hash-object")

class gitRepo(object):
    workTree=None
    gitDir=None
    conf=None
    def __init__(self,path,force=false):
        self.workTree=path
        self.gitDir=os.pardir.join(self.workTree,".git")
        if not (force or os.path.isdir(self.gitDir)):
            raise Exception("No git directory found")
        self.conf=configparser.ConfigParser()
        cf=repo_file(self,conf)
        if cf and os.path.exists(cf):
            self.conf.read([cf])
        elif not force:
            raise Exception("Config File missing")
        if not force:
            ver=int(self.conf.get("core","repoFormatted"))
            if ver!=0:
                raise Exception("Version not supported")




def main(argv=sys.argv[1:]):
    args=argParser.parse_args(argv)
    match args.command:
        case "add"          : cmd_add(args)
        case "cat-file"     : cmd_cat_file(args)
        case "check-ignore" : cmd_check_ignore(args)
        case "checkout"     : cmd_checkout(args)
        case "commit"       : cmd_commit(args)
        case "hash-object"  : cmd_hash_object(args)
        case "init"         : cmd_init(args)
        case "log"          : cmd_log(args)
        case "ls-files"     : cmd_ls_files(args)
        case "ls-tree"      : cmd_ls_tree(args)
        case "rev-parse"    : cmd_rev_parse(args)
        case "rm"           : cmd_rm(args)
        case "show-ref"     : cmd_show_ref(args)
        case "status"       : cmd_status(args)
        case "tag"          : cmd_tag(args)
        case _              : print("Bad command.")
        