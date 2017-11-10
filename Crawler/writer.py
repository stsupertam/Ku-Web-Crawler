import os
import csv
import sys
import hashlib
import requests
from colorama import init
from colorama import Fore
from bs4 import BeautifulSoup
from urllib.parse import unquote


class Writer:

    def __init__(self):
        init(autoreset=True)
        self.files = 0

    def writeRobotsToFile(self, domain, domain_robots, scheme):
        try:
            robot = requests.get(('%s://%s/robots.txt' % (scheme, domain)), timeout=(5,5))
            robot_code = robot.status_code
            if(robot_code == requests.codes.ok):
                domain_robots[domain] = True
                print(Fore.GREEN + 'Robots.txt is Found in [%s]' % (domain))
                with open('./robotlists.txt', 'a') as file:
                    file.write(domain + '\n')
            else:
                print(Fore.RED + 'Couldn\'t Find Robots.txt [%s]' % (domain))
        except Exception:
            print(Fore.RED + 'Couldn\'t Get Robots.txt [Error Exception : %s] [%s]' % (sys.exc_info()[0], domain))
        return domain_robots

    def writeToFile(self, domain, path, soup):
        try:
            html = soup.prettify('utf-8')
        except Exception:
            print(Fore.RED + 'Soup Error [Error Exception : %s] [%s]' % (sys.exc_info()[0], domain))
            return

        if(path == '' or path == '/'):
            html_file = 'index.html'
        else:
            if(path[0] == '/'):
                path = path[1:]
            if(path[-1] == '/'):
                path = path[0:len(path) - 1]

        path_split = path.split('/')
        html_file = path_split[-1]

        if('.' in html_file):
            path_split.pop(-1)
        else:
            html_file = 'index.html'

        path = str.join('/', path_split)
        directory = self.createDirectory(domain, path)

        fileName = directory + '/' + html_file

        print(Fore.GREEN + 'Create file in [%s] [%s] : [%s]' % (directory, fileName, path))
        try:
            with open(fileName, "wb") as file:
                file.write(html)
                self.files += 1
        except Exception:
            print(Fore.RED + 'Write to file error [Error Exception : %s]' % (sys.exc_info()[0]))

    def createDirectory(self, domain, path):
        directory = 'html/' + domain
        path = unquote(path)
        os.makedirs(directory, exist_ok=True)

        if(len(path) != 0 and len(path) != 1):
            path_split = path.split('/')
            if(path_split[0] == ''):
                path_split.pop(0)
            elif(path_split[-1] == ''):
                path_split.pop(-1)
            path = str.join('/', path_split)
            if(path == '' or path == '/'):
                directory = directory
            else:
                directory = directory + '/' + path
            try:
                os.makedirs(directory, exist_ok=True)
            except Exception:
                print(Fore.RED + 'Create Directory error [Error Exception : %s]' % (sys.exc_info()[0]))
        return directory

