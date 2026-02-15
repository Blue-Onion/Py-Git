from repo.core import repoCreate

def cmdInit(args):
    repoCreate(args.path)

def setup(subparsers):
    argsp=subparsers.add_parser("init",help="Intialize new repo")
    argsp.add_argument("path",metavar="dir",nargs="?",default=".",help="Create new repo")
