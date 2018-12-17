from bs4 import BeautifulSoup
from urllib import request

req = request.Request(url="http://www.qyl82.com/92096/")

html = request.urlopen(req)

bs_obj = BeautifulSoup(html.read(), "html.parser")
video_div = bs_obj.find('div',id='player-container').video.source.get("src")
print(video_div)