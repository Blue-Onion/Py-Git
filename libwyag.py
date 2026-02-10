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
argSubParser.add_parser("add")
argSubParser.add_parser("cat-file")
argSubParser.add_parser("check-ignore")
argSubParser.add_parser("checkout")
argSubParser.add_parser("commit")
argSubParser.add_parser("hash-object")

def main(argv=sys.argv[1:]):
    args=argParser.parse_args(argv)
    match args.command:
        case "add": print("Joseph Vissarionovich Stalin[e][f] (né Dzhugashvili;[g] 18 December [O.S. 6 December] 1878 – 5 March 1953) was a Soviet revolutionary and politician who led the Soviet Union from 1924 until his death in 1953.")
        case "cat-file": print("""
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣠⣴⣶⣶⣶⣶⣿⣿⣶⣶⣶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⠟⠙⣿⣿⠈⣿⣿⣿⠟⠟⣿⣿⣿⣿⣿⣯⣇⣿⣿⣿⡏⣀⣩⡿⢿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⠋⣫⢁⣄⣿⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣄⣘⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣶⣿⣿⣿⡿⠿⠿⢿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠘⢿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⠋⠉⠀⠀⠀⠀⠀⠀⠈⠉⠉⠛⠛⠛⠛⠙⠻⠛⠉⠉⠉⠉⠙⠛⢿⣿⣿⣇⣀⣠⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⢿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣯⠉⢿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣦⡀⠹⢿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⡄⢨⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⢃⣠⣶⣿⣿⣶⣤⣤⣄⣀⠀⠀⠀⠀⠀⣀⣤⣴⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⢤⣽⣓⠻⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⣿⡿⠁⢀⣀⣈⣉⣻⣿⡿⠁⠀⠀⠀⢸⣿⣿⠟⡩⠿⣶⣤⣉⡙⠿⣿⡄⠀⠀⠀⠀⠀⢸⣿⣿⡃⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡇⠉⠀⣴⣶⣿⣿⠻⣿⣿⣿⡆⠀⠀⠀⠘⣿⣿⣾⣷⣿⣿⣿⣿⣿⣶⣍⠁⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⡇⠀⠀⠏⠉⠉⠁⢠⣾⣿⠟⠀⠀⠀⠀⠀⠘⢿⣿⣿⣌⠭⢬⣧⡀⠉⠛⠃⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⠃⠀⠀⠀⠐⠒⢚⡭⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠻⠿⠶⠾⣟⡉⠀⠀⠀⠀⠀⠀⠀⠀⠸⠟⣣⢷⣾⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⡀⠀⠀⠀⠀⠀⠉⠀⠀⢀⡆⠀⠀⠀⠀⠀⠀⠀⣼⣦⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡉⠀⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⣴⡟⢀⠀⢀⣀⠀⠀⠀⠀⢻⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡆⢻⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡇⠀⠀⠀⠀⠀⢀⣼⠟⠶⠿⠆⣼⣿⡟⠰⠾⢷⡾⠿⣿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⡇⣾⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⢿⡇⠀⠀⠀⠀⢀⡾⠉⠀⣀⣀⣀⣭⣿⢿⣿⠷⣶⣷⣦⣜⣿⠿⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠟⠉⣼⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⡇⠀⠀⠀⠰⠇⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⢿⣿⣿⣤⠙⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣇⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣟⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⢸⣷⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡀⢦⣤⣾⣿⣿⣿⣿⣿⠿⠛⠛⠛⠛⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡶⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣇⠀⠙⠛⠻⣿⠟⠋⠀⠀⢀⣠⣾⣿⣿⣿⣿⠛⠛⠛⠛⠛⠛⠛⠉⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣄⠀⠀⠀⠁⠀⠀⠀⠀⠘⠿⠿⠿⠿⠿⠿⠓⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⡳⣄⢀⠀⠀⠀⠀⠀⠀⢀⣤⣤⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣿⣿⣿⣯⣻⢿⣷⣦⣤⣤⣶⣿⣿⣿⣿⣿⣿⣦⠀⢀⣀⣠⠴⠄⠀⠀⠀⠀⠀⣾⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⡳⣯⡻⠛⠛⠿⠿⠿⣿⣿⣿⣿⣿⠿⠋⠉⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡹⣦⠀⠀⠀⠀⠈⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣷⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⣀⣀⣤⣴⡾⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣮⡳⣤⡀⠀⠀⢻⣿⣿⣿⡆⠀⠀⠀⠀⠀⢀⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣤⣀⡀⠀⠀⠀⠀
            ⠀⢀⣠⣴⣶⣿⣿⣿⡿⢟⣳⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣦⣍⠲⢤⡀⠈⠙⢿⣇⠀⠀⠀⣀⡴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡾⣿⣿⣿⣿⣿⣷⣦⣀⠀
            ⢿⣿⣿⣿⡿⢟⣻⣥⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣵⣌⠻⣿⣿⣿⣿⣿⣿⣿⣦⡙⠳⣤⣼⣧⣀⡤⢚⣵⣾⣿⣿⣿⣿⣿⢏⡛⠿⣿⣿⣿⣿⣿⣿⣷⣶⣿⣽⣿⣿⣿⣿⣿⠇
            ⠀⠙⠛⠻⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢏⣾⡿⢿⣷⡽⣿⣿⣿⣿⣿⣿⣿⣿⣷⢲⣤⣽⣥⣾⣿⣿⣿⣿⣿⣿⣿⡟⢸⡿⠳⣌⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀
            ⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⡁⢀⣼⠀⣿⡟⢿⣿⣿⣿⣿⣿⣿⣿⡀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⡀⢀⡙⢻⡄⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠈⠉⠛⠻⠿⢿⣿⣿⣿⣿⣿⣿⣮⢳⣾⣧⣾⣿⣿⣎⢿⣿⣿⣿⣿⣿⡿⠁⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⣿⣿⣾⣷⣿⠇⣿⣿⣿⣿⡿⠛⠉⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣦⡻⣿⣿⣿⠟⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⠀⣿⣿⡟⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣽⠟⠁⢀⣾⣿⣿⡄⢠⣿⣿⣿⣿⣿⣿⣿⠃⣼⣿⣿⣿⣿⡇⠀⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            """)
        case "check-ignore": print("Epstein was the first of two children born to Paula Epstein (née Stolofsky) and Seymour Epstein, who were themselves children of Jewish immigrants.")
        case "checkout": print("In 1974, despite not having a degree, Epstein began teaching physics and mathematics at the prestigious Dalton School in Manhattan, New York, many of whose students belonged to some of the wealthiest families in the country. ")
        case "commit": print("Even as he was climbing the ladder at Bear Stearns and mingling with some of New York’s, and the world’s, wealthiest movers and shakers, there were warning signs of inappropriate behavior. ")
        case "hash-object":print("Hello")
        