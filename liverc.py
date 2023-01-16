import requests, re
from datetime import datetime
m3ufile=open("liverc.m3u","w",encoding="utf-8")
headers = {
            'authority': 'live.liverc.com',
            'accept-encoding': 'gzip, deflate, br',
            'cache-control': 'max-age=0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
            'referer': 'https://mmrdirect.liverc.com/'
            }
url="https://live.liverc.com/"
page = requests.get(url, headers=headers)
trackweblocation=re.findall(r"<i class=\"fa fa-video-camera fa-fw status_video_1\"><\/i>\n\t\t\t\t\t\t\t\t\t\t\t\t<i class=\".*?\"><\/i>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<br \/><small><small>.*?<\/small><\/small>\n\t\t\t\t\t\t\t\t\t\t\t<\/td>\n\t\t\t\t\t\t\t\t\t\t\t<td><span class=\"hidden\">seRC<\/span><a href=\"(.*?)\"><strong>.*?<\/strong><\/a><div class=\"indent\"><small>.*?<\/small>",page.text)
tracklocation=re.findall(r"<i class=\"fa fa-video-camera fa-fw status_video_1\"><\/i>\n\t\t\t\t\t\t\t\t\t\t\t\t<i class=\"\*?\"><\/i>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<br \/><small><small>.*?<\/small><\/small>\n\t\t\t\t\t\t\t\t\t\t\t<\/td>\n\t\t\t\t\t\t\t\t\t\t\t<td><span class=\"hidden\">seRC<\/span><a href=\".*?\"><strong>(.*?)<\/strong><\/a><div class=\"indent\"><small>.*?<\/small>",page.text)
trackvenue=re.findall(r"<i class=\"fa fa-video-camera fa-fw status_video_1\"><\/i>\n\t\t\t\t\t\t\t\t\t\t\t\t<i class=\".*?\"><\/i>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<br \/><small><small>.*?<\/small><\/small>\n\t\t\t\t\t\t\t\t\t\t\t<\/td>\n\t\t\t\t\t\t\t\t\t\t\t<td><span class=\"hidden\">seRC<\/span><a href=\".*?\"><strong>.*?<\/strong><\/a><div class=\"indent\"><small>(.*?)<\/small>",page.text)
#print(trackweblocation[0])
#m3ufile.write("#EXTM3U")
m3ufile.write("\n")
currenttime = datetime.now()
logo="https://www.liverc.com/static/lrc/liverc_logo.png"
#datehour = int(currenttime.strftime("%I"))
#print(datehour)
#print(str(datehour))
datetimestring = currenttime.strftime("Updated: %m/%d/%Y %I:%M%p EST")
print(datetimestring)
m3ufile.write("\n#EXTINF:-1 tvg-id=\"LiveRCInfo.us\" tvg-logo=\""+logo+"\" group-title=\"LiveRC 🏎️\","+datetimestring+"\nhttp://blah.com/playlist.m3u8")
for i in range(0,200,1):
    try:           
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}
        suburl="https:"+trackweblocation[i]+"live/video/"
        page2 = requests.get(suburl, headers=headers)
        trackname=re.findall(r"\"name\":\"(.*?)\",\"address",page2.text)
        idnumber = re.findall(r"videoID = '(.*?)';",page2.text)
        print(str(i)+" - "+trackname[0])
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}
        suburl3="https:"+trackweblocation[i]
        page3 = requests.get(suburl3, headers=headers)                
        try:
            if trackname[0].islower() == True:
                tvstring=trackname[0].title()+": "+trackvenue[i]   
            else:
                tvstring=trackname[0]+": "+trackvenue[i]            
        except:
            if trackname[0].islower() == True:
                tvstring=trackname[0].title()
            else:
                tvstring=trackname[0]
        print(tvstring)
        try:
            tracklogo=re.findall(r"<img src=\"(https:\/\/assets\.livetimescoring\.com\/track_logos.*?)\">",page3.text)
            m3ufile.write("\n#EXTINF:-1 tvg-id=\"LiveRC.us\" tvg-logo=\""+tracklogo[0]+"\" group-title=\"LiveRC 🏎️\","+tvstring+"\nhttps://5e3e097661a96.streamlock.net/liverc_broadcast/mp4:liverc_Camera1_"+idnumber[0]+"/playlist.m3u8")
        except:            
            m3ufile.write("\n#EXTINF:-1 tvg-id=\"LiveRC.us\" tvg-logo=\""+logo+"\" group-title=\"LiveRC 🏎️\","+tvstring+"\nhttps://5e3e097661a96.streamlock.net/liverc_broadcast/mp4:liverc_Camera1_"+idnumber[0]+"/playlist.m3u8")
    except: continue
m3ufile.close()
