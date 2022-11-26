class Urls:
    def __init__(self, group_name, token, ver_api):
        self.group_name = group_name
        self.token = token
        self.ver_api = ver_api

    def url_get_group_id(self):
        url = f'https://api.vk.com/method/wall.get?domain={self.group_name}' \
                f'&count=100&offset=1&access_token={self.token}&v={self.ver_api}'
        return url

    def url_get_server(self, group_id):
        url = f'https://api.vk.com/method/photos.getWallUploadServer?' \
            f'group_id={group_id}&access_token={self.token}&v={self.ver_api}'
        return url

    def url_save_photo(self, group_id, photo, server, hash):
        url = f'https://api.vk.com/method/photos.saveWallPhoto?access_token={self.token}' \
            f'&group_id={group_id}&photo={photo}&server={server}&hash={hash}&v={self.ver_api}'
        return url

    def url_publish_post(self, group_id, photos, text, date=None):
        if date == None:
            url = f'https://api.vk.com/method/wall.post?owner_id=-{group_id}' \
                f'&attachments={photos}&message={text}&from_group=1&access_token={self.token}&v={self.ver_api}'
        else:
            url = f'https://api.vk.com/method/wall.post?owner_id=-{group_id}' \
                f'&attachments={photos}&message={text}&publish_date={date}&from_group=1&access_token={self.token}&v={self.ver_api}'
        return url