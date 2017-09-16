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

    def writeRobotsToFile(self, domain, domain_robots):
        try:
            robot = requests.get(('%s://%s/robots.txt' % (self.scheme, domain)), timeout=(5,5))
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

    def writeHashMatching(self, directory, hash, url):
        csvFile = directory + '/hash_matching.csv'
        if(not os.path.isfile(csvFile)):
            try:
                with open(csvFile, 'w', newline='') as f:
                    fieldnames = ['hash', 'url']
                    writer = csv.writer(f)
                    writer.writerow(fieldnames)
            except Exception:
                print(Fore.RED + 'Create new file error [Error Exception : %s]' % (sys.exc_info()[0]))
        try:
            with open(csvFile, 'a', newline='') as f:
                fieldnames = [hash, url]
                writer = csv.writer(f)
                writer.writerow(fieldnames)
        except Exception:
            print(Fore.RED + 'Write hash to file error [Error Exception : %s]' % (sys.exc_info()[0]))

    def writeToFile(self, domain, path, url, soup):
        directory = self.createDirectory(domain, path)
        html = soup.prettify('utf-8')
        h = hashlib.md5(html).hexdigest()
        fileName = directory + '/' + h + '.html'

        self.writeHashMatching(directory, h, url)
        self.files += 1
        print(Fore.GREEN + 'Create file [%d] : [%s]' % (self.files, h))
        try:
            with open(fileName, "wb") as file:
                file.write(html)
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
            path_split.pop(-1)
            path = str.join('/', path_split)
            directory = directory + '/' + path
            os.makedirs(directory, exist_ok=True)
        return directory
