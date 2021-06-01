import os
# https://www.runoob.com/python/os-file-methods.html

music_form = {'MP3','WMA','WAV','APE','FLAC','OGG','AAC'}

# coding=gb2312
def readMusicFromFolder(path):
    try:
        result = []
        for root, dirs, files in os.walk(path):
            for name in files:
                music_name = os.path.join(root, name)

                # Get rid of other data
                if(music_name[music_name.rfind('.') + 1:].upper() in music_form):
                    result.append(music_name)

        return result
    except Exception as e:
        print(e)
        return []


def readMusicFromList(path_list):
    result = []
    for folder in path_list:
        result += readMusicFromFolder(folder)
    return result

def readDir(file_name):
    f = open(file_name, 'r')
    result = []
    current_dir = f.readline()
    while(current_dir != ""):
        result.append(current_dir.strip())
    f.close()
    return result


def updateDir(file_name, new_data):
    f = open(file_name, 'w')
    for line in new_data:
        f.write(line)
    f.close()


if __name__ == "__main__":
    musics = readMusicFromFolder("E:/CloudMusic")
    for i in musics:
        print(i.decode('gbk', errors='ignore'))
    