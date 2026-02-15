import os
import configparser

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
