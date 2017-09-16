import sys
import requests
from colorama import init
from colorama import Fore
from urllib import robotparser

class RobotParser():

    def __init__(self):
        init(autoreset=True)
        self.scheme = 'http'

    def writeRobotsToFile(self, domain):
            robot = requests.get(('%s://%s/robots.txt' % (self.scheme, domain)), timeout=5)
            robot_code = robot.status_code
            if(robot_code == requests.codes.ok):
                print(Fore.GREEN + 'Robots.txt is Found in [%s]' % (domain))
                with open('./robotlists.txt', 'a') as file:
                    file.write(domain + '\n')
            else:
                print(Fore.RED + 'Couldn\'t Find Robots.txt [%s]' % (domain))
            print(Fore.RED + 'Couldn\'t Get Robots.txt [Error Exception : %s] [%s]' % (sys.exc_info()[0], domain, ))

    def canFetchUrl(self, domain, url):
        try:
            rp = robotparser.RobotFileParser()
            rp.set_url('%s://%s/robots.txt' % (self.scheme, domain))
            rp.read()
            if(not rp.can_fetch('*', ('%s://%s%s' % (self.scheme, domain, url)))):
                return False
            else:
                return True
        except Exception:
            print(Fore.RED + 'Couldn\'t Fetch Robots.txt [Error Exception : %s] [%s]' % (sys.exc_info()[0], domain))
            return True
