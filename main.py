from parse_posts import Parse
from utils.common import get_data_from_yaml, Wotemark
import argparse
from tqdm import tqdm
import os
import time

def main(args):
    config = get_data_from_yaml(args.config)
    parse = Parse(config)

    for i in tqdm(range(config.general.circles)):
        parse.start()
        config.general.offset += 200

    if args.wotemark:
        wotemark = Wotemark(config.general.logo)
        for post in os.listdir(f'data/{config.general.group_name}/images'):
            path  = f'data/{config.general.group_name}/images/{post}'
            for item in os.listdir(f'data/{config.general.group_name}/images/{post}'):
                wotemark.wotermark(os.path.join(path, item), path, item)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, default='configs/config.yaml', help='Путь до конфиг файла')
    parser.add_argument('--wotemark', type=bool, default=True, help='Добавление водяного знака.')
    args = parser.parse_args()
    start_time = time.time()
    main(args)
    print("--- %s seconds ---" % (time.time() - start_time))
