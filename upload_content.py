import requests
import os
from utils.get_urls import Urls
from utils.common import get_data_from_yaml

class Upload_posts:
    def __init__(self, config):
        self.config = get_data_from_yaml(config)
        self.group_name = self.config.general.group_name
        self.dir_name = self.config.general.dir_name
        self.urls = Urls(self.group_name, self.config.general.token, self.config.general.ver_api)
        self.group_id = self.__get_group_id()
        
    
    def __get_group_id(self):
        req = requests.get(self.urls.url_get_group_id()).json()
        return abs(req['response']['items'][1]['owner_id'])
    
    def __upload_photo_server(self, file, list_photos: list):
        try:
            upload_url = requests.get(self.urls.url_get_server(self.group_id)).json()['response']['upload_url']
        except Exception as e:
            print(f'Exception {e}')
        req_post = requests.post(upload_url, files=file).json()
        photo, server, hash = req_post['photo'], req_post['server'], req_post['hash']
        succes_load = requests.get(self.urls.url_save_photo(self.group_id, photo, server, hash)).json()
        owner_id, photo_id = succes_load['response'][0]['owner_id'], succes_load['response'][0]['id']
        list_photos.append(f'photo{owner_id}_{photo_id}')
        return list_photos

    def __list_photo_server(self, path_to_post):
        list_photos, file = [], {}
        for item in os.listdir(path_to_post):
            item = os.path.join(path_to_post, item)
            with open(item, 'rb') as photo:
                file['photo'] = photo
                list_photos = self.__upload_photo_server(file, list_photos)
        return list_photos

    def __publish_post(self, photos: list, text_file):
        photos_str = ''
        for num, item in enumerate(photos):
            if num == (len(photos)-1):
                photos_str += item
            else:
                photos_str += f'{item}, '
        req = requests.get(self.urls.url_publish_post(self.group_id, photos_str, text_file))
        # print(req.status_code)
    
    def start(self):
        path = f'data/{self.dir_name}/images'
        for item in os.listdir(path):
            with open(f'data/{self.dir_name}/text/{item}.txt', 'r') as file:
                text_file = file.read()
                if len(text_file) > 3000:
                    continue
            path_post = os.path.join(path, item)
            photos = self.__list_photo_server(path_post)
            self.__publish_post(photos, text_file)

    
if __name__ == '__main__':
    ss = Upload_posts('configs/config.yaml')
    ss.start()