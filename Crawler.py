from ExtractLinks import ExtractLinks

linkParser = ExtractLinks('ku')
depth = 5
urls = []
for i in range(1, depth + 1):
    urls[i] = []

#urls = {}
urls[0] = linkParser.get_link('ku.ac.th/web2012/index.php?c=adms&m=mainpage1')
#
#for key in urls:
#    for item in urls[key]:
#        urls['2'] = 'Gundam'
#        print("Url Depth %s : %s" % (key, item))