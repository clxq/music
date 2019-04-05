import requests
import json


def search_songs(songname):
    url = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.song&searchid=64336222123454546&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=20&w={}&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0".format(songname)
    # 获取网页源码
    html = requests.get(url).text
    return html


# 加载动态文件    str-->dict--字典
def get_json(html):
    # 将字符串转json文本数据进行操作
    json_data = json.loads(html, encoding='utf-8')
    # print(json_data)
    return json_data


# 用来存储搜索到的每一首歌曲的albummid、歌名
albummid_list = []
songname_list = []


# 获取歌曲列表
def get_songs(json_data):
    song_list = json_data['data']['song']['list']
    # print(song_list)
    for index in range(len(song_list)):
        song_name = song_list[index]["title"]
        singer_name = song_list[index]["singer"][0]["name"]
        song_album = song_list[index]["album"]["name"]
        song_time = song_list[index]["interval"]
        song_albummid = song_list[index]['album']['mid']
        albummid_list.append(song_albummid)
        songname_list.append(song_name)
        print(index + 1, "》》", song_name, singer_name, song_album, song_time)


# 下载指定歌曲
def download_song(number):
    print("Download......")
    albummid = albummid_list[number - 1]
    url1 = "https://c.y.qq.com/v8/fcg-bin/fcg_v8_album_info_cp.fcg?albummid={}&g_tk=5381&loginUin=0&hostUIn=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0".format(albummid)
    res1 = requests.get(url1).text
    # print(res1)
    json_data1 = json.loads(res1, encoding='utf-8')
    # print(json_data1)
    # 获取songmid
    album_list = json_data1['data']['list']
    for i in range(len(album_list)):
        songmid1 = album_list[i]["songmid"]
        # print(songmid1)
    url2 = 'https://u.y.qq.com/cgi-bin/musicu.fcg?-=getplaysongvkey551236458755685&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8' \
           '&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data={"req":{"module":"CDN.SrfCdnDispatchServer","method":"GetCdnDispatch","param":{"guid":"6767512396","calltype":0,"userip":""}},' \
           '"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"6767512396","songmid":["%s"],"songtype":[0],"uin":' \
           '"0","longinflag":1,"platform":"20"}},"comm":{"uin":0,"format":"json","ct":20,"cv":0}}' % songmid1
    res2 = requests.get(url2).text
    json_data2 = json.loads(res2, encoding='utf-8')
    # print(json_data2)
    # 获取purl
    purl_list = json_data2['req_0']['data']['midurlinfo']
    for i in range(len(purl_list)):
        song_purl = purl_list[i]["purl"]
        # print(song_purl)
        preurl = "http://183.222.96.18/amobile.music.tc.qq.com/"
        # 载url
        real_url = preurl + song_purl
        #下载歌曲
        song_bytes = requests.get(real_url).content  # 字节
        songname = songname_list[number - 1]
        songfile = open("D:\\爬虫存储\\%s.m4a" % songname, "wb")
        songfile.write(song_bytes)
        print("下载成功ヾ(@^▽^@)ノ")


if __name__ == '__main__':
    songname = input("请输入歌名：")
    html = search_songs(songname)
    json_data = get_json(html)
    get_songs(json_data)
    number = int(input("\n请输入要下载的歌曲序号:"))
    while number < 1:
        number = int(input("\n请重新输入要下载的歌曲序号:"))
    download_song(number)
