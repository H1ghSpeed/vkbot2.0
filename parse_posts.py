import json
import requests
import os
import asyncio, aiofiles
from tqdm import tqdm

class Parse:
    def __init__(self, config):
        self.config = (config)
        self.group_name = self.config.general.group_name
        self.offset = self.config.general.offset
        self.folder = f'data/{self.group_name}'
        self.wall_posts = []
        for i in range(self.config.general.circles):
            url = f'https://api.vk.com/method/wall.get?domain={self.group_name}' \
                        f'&count=100&offset={self.offset}&access_token={self.config.general.token}&v=5.131'
            walls = self.__response_json(url)
            self.wall_posts.append(walls['response']['items'])
            self.offset += 100

    def __response_json(self, url):
        get_wall = requests.get(url).json()
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)
        if not os.path.exists(f'{self.folder}/images'):
            os.mkdir(f'{self.folder}/images')
            os.mkdir(f'{self.folder}/text')
        return get_wall
    
    async def __save_image(self, image_url:str, post_id:int, count:int):
        path = f'{self.folder}/images/{post_id}'
        result_image = requests.get(image_url)
        async with aiofiles.open(f'{path}/{post_id}_{count}.jpg', 'wb') as file:
            await file.write(result_image.content)

    async def __save_text(self, text, post_id):
        async with aiofiles.open(f'{self.folder}/text/{post_id}.txt', 'w', encoding='utf-8') as file:
            try:
                await file.write(text)
            except Exception:
                pass

    def __start_async(self, post_id: int, text: str, images: list):
        event_loop = asyncio.get_event_loop()
        tasks = []
        for count,image in enumerate(images):
            tasks.append(asyncio.ensure_future(self.__save_image(image, post_id, count)))
        tasks.append(self.__save_text(text, post_id))
        event_loop.run_until_complete(asyncio.gather(*tasks))
    
    def start(self):
        for circle in tqdm(self.wall_posts, position=0, leave=False):
            for post in tqdm(circle, position=1, leave=False):
                save_post = True
                images = []
                if 'attachments' in post:
                    post_id, text, attach = post['id'], post['text'], post['attachments']
                    for i in self.config.general.stop_slova.split(','):
                        if i in text or text == '':
                            save_post = False
                            break
                if save_post:
                    if not os.path.exists(f'{self.folder}/images/{post_id}'):
                        os.mkdir(f'{self.folder}/images/{post_id}')
                    for photo in attach:
                        if photo['type'] == 'photo':
                            url_photo = photo['photo']['sizes'][-1]['url']
                            images.append(url_photo)
                    self.__start_async(post_id, text, images)