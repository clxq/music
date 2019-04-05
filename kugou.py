import requests, json


def search_song(songname):
    url = "https://songsearch.kugou.com/song_search_v2?callback=jQuery1124042119196110168566_1546054478444&keyword=(%s)&pagesize=30&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filter=0" % songname
    rsp = requests.get(url)
    # 获取网页源码
    html = rsp.text
    # print(html)
    return html  # str


# 加载动态文件    str-->dict--字典
def get_json(html):
    start = html.find("{")
    json_text = html[start:-2]
    json_data = json.loads(json_text, encoding="utf-8")
    # print(json_data)
    return json_data


# 用来存储搜索到的每一首歌曲的id、歌名
songid_list = []
songname_list = []

# 获取歌曲信息
def get_songs(json_data):
    # 歌曲详情
    songs = json_data["data"]["lists"]
    print("\n搜索歌曲信息如下：")
    for index in range(len(songs)):
        # print(index)
        album = songs[index]["AlbumName"]  # 专辑名
        song = songs[index]["FileName"]  # 歌曲名
        time = songs[index]["Duration"]  # 时长
        filehash = songs[index]["FileHash"]  # 歌曲id
        songname_list.append(song)
        songid_list.append(filehash)
        print(index + 1, ">>>", song, album, time)


# 下载指定歌曲
def download_song(number):
    print("Download......")
    songid = songid_list[number - 1]
    song_information = "https://wwwapi.kugou.com/yy/index.php?r=play/getdata&hash=%s" % songid
    # 下载网页，获取源码，json--play_url
    song_text = requests.get(song_information).text
    song_json = json.loads(song_text, encoding="utf-8")
    play_url = song_json["data"]["play_url"]
    # print(play_url)
    # 下载歌曲
    song_bytes = requests.get(play_url).content  #字节
    songname=songname_list[number-1]
    songfile = open("D:\\爬虫存储\\%s.mp3"%songname,"wb")
    songfile.write(song_bytes)
    print("下载成功")

if __name__ == '__main__':
    songname = str(input("请输入要搜索的歌曲:"))
    html = search_song(songname)
    json_data = get_json(html)
    get_songs(json_data)
    number = int(input("\n请输入要下载的歌曲序号:"))
    while number < 1:
        number = int(input("\n请重新输入要下载的歌曲序号:"))
    download_song(number)
