from parse_posts import Parse
from utils.common import get_data_from_yaml, Wotemark
import argparse
from tqdm import tqdm
import os
import time

def main(args):
    config = get_data_from_yaml(args.config)
    parse = Parse(config)
    parse.start()

    if config.general.wotemark:
        wotemark = Wotemark(config.general.logo)
        for post in os.listdir(f'data/{config.general.group_name}/images'):
            path  = f'data/{config.general.group_name}/images/{post}'
            for item in tqdm(os.listdir(f'data/{config.general.group_name}/images/{post}'), position=0, leave=False):
                wotemark.wotermark(os.path.join(path, item), path, item)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, default='configs/config.yaml', help='Путь до конфиг файла')
    args = parser.parse_args()
    start_time = time.time()
    main(args)
    print("--- %s seconds ---" % (time.time() - start_time))
