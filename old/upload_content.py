import shutil
from auth_data import token
import requests
import os
from tqdm import tqdm

def server(group_id, file, spisok_postov):
    try:
        url = f'https://api.vk.com/method/photos.getWallUploadServer?group_id={group_id}&access_token={token}&v=5.131'
        request = requests.get(url).json()
        upload_url = request['response']['upload_url']
        ur = requests.post(upload_url, files=file).json()
        photo, serve, hash = ur['photo'], ur['server'], ur['hash']
        url1 = f'https://api.vk.com/method/photos.saveWallPhoto?access_token={token}&group_id={group_id}&photo={photo}&server={serve}&hash={hash}&v=5.131'
        rq = requests.get(url1).json()
        owner_id = rq['response'][0]['owner_id']
        photo_id = rq['response'][0]['id']
        spisok_postov.append(f'photo{owner_id}_{photo_id}')
    except Exception as e:
        print(e)


def group_id(group_name):
    url = f'https://api.vk.com/method/wall.get?domain={group_name}&count=100&offset=1&access_token={token}&v=5.131'
    req = requests.get(url)
    src = req.json()
    global group_id
    group_id = abs(src['response']['items'][1]['owner_id'])


def post(photos, text, date1=None):
    try:
        if date1 == None:
            url = f'https://api.vk.com/method/wall.post?owner_id=-{group_id}&attachments={photos}&message={text}&from_group=1&access_token={token}&v=5.131'
        else:
            url = f'https://api.vk.com/method/wall.post?owner_id=-{group_id}&attachments={photos}&message={text}&publish_date={date1}&from_group=1&access_token={token}&v=5.131'
        rq = requests.get(url)
        print(photos, post_id)
        # print(rq)

    except Exception:
        print(f'Ошибка с постом {post_id}, идём дальше')
        print(Exception)


def rm_post(text_file, photo_file):
    os.remove(text_file)
    shutil.rmtree(photo_file)
    print(f'Удаление поста {text_file} успешно')


if __name__ == '__main__':
    # date1 = 1666764619
    # group_name = input('Введите название группы, куда делать постинг: ')
    group_name = 'deti_tmij'
    group_id(group_name)
    l2 = []
    # dir_name = input('Введите название папки: ')
    dir_name = 'godless_dependence'
    for list1 in tqdm(os.listdir(f'{dir_name}/files'), position=0, leave=False):
        post_id, file, spisok_postov = list1, {}, []
        l2.append(list1)
        src = ''
        text = ''
        try:
            text = open(f'{dir_name}/text/{post_id}.txt')
            text = text.read()
        except Exception:
            pass
        for item in os.listdir(f'{dir_name}/files/{post_id}'):
            file['photo'] = open(f'{dir_name}/files/{post_id}/{item}', 'rb')
            server(group_id, file, spisok_postov)
        for i in range(len(spisok_postov)):
            if len(spisok_postov) == 1:
                src = spisok_postov[i]
            else:
                if i != len(spisok_postov) - 1:
                    src = src + spisok_postov[i] + ', '
                else:
                    src = src + spisok_postov[i]
        post(src, text)
        # date1 += 3600
        # rm_post(f'{dir_name}/text/{post_id}.txt',f'{dir_name}/files/{post_id}')
    print(l2)
