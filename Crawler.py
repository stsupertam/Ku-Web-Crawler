from ExtractLinks import ExtractLinks

linkParser = ExtractLinks('ku.ac.th/web2012/index.php?c=adms&m=mainpage1', 'ku')
ku_url = linkParser.get_link()
for item in ku_url:
    print('Url : ' + item)

linkParser = ExtractLinks('http://ku.ac.th/web2012/index.php?c=adms&m=changepage&page=home&lang=eng', 'ku')
ku_url = linkParser.get_link()
for item in ku_url:
    print('Url : ' + item)

linkParser = ExtractLinks('https://stackoverflow.com/questions/6797984/how-to-convert-string-to-lowercase-in-python', 'ku')
ku_url = linkParser.get_link()

for item in ku_url:
    print('Url : ' + item)