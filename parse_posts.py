import json
import requests
import os
import asyncio, aiohttp, aiofiles

class Parse:
    def __init__(self, config):
        self.config = (config)
        self.group_name = self.config.general.group_name
        self.url = f'https://api.vk.com/method/wall.get?domain={self.group_name}' \
                    f'&count=100&offset={self.config.general.offset}&access_token={self.config.general.token}&v=5.131'
        self.folder = f'data/{self.group_name}'
        walls = self.__response_json()
        self.wall_posts = walls['response']['items']

    def __response_json(self):
        get_wall = requests.get(self.url).json()
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)
        if not os.path.exists(f'{self.folder}/images'):
            os.mkdir(f'{self.folder}/images')
            os.mkdir(f'{self.folder}/text')
        return get_wall
    
    async def __save_images(self, images, post_id):
        path = f'{self.folder}/images/{post_id}'
        if not os.path.exists(path):
            os.mkdir(path)

        for count, image_url in enumerate(images):
            result_image = requests.get(image_url)
            async with aiofiles.open(f'{path}/{post_id}_{count}.jpg', 'wb') as file:
                await file.write(result_image.content)


    async def __save_text(self, text, post_id):
        async with aiofiles.open(f'{self.folder}/text/{post_id}.txt', 'w') as file:
            try:
                await file.write(text)
            except Exception:
                pass

    async def __start_async(self, post_id: int, text: str, images: list):
        await self.__save_images(images, post_id)
        await self.__save_text(text, post_id)
    
    def start(self):
        for post in self.wall_posts:
            images = []
            if 'attachments' in post:
                post_id, text, attach = post['id'], post['text'], post['attachments']
            for photo in attach:
                if photo['type'] == 'photo':
                    url_photo = photo['photo']['sizes'][-1]['url']
                    images.append(url_photo)
            asyncio.run(self.__start_async(post_id, text, images))