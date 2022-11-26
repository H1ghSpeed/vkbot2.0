import os


def main(dir_name):
    l2 = []
    for list1 in os.listdir(f'{dir_name}/text'):
        s = ''
        l2.append(list1)
        try:
            with open(f'{dir_name}/text/{list1}', 'r') as text_file:
                text = text_file.readlines()
                for i in text:
                    if i == 'ATMOSPHERE':
                        pass
                    else:
                        s+=i
            with open(f'{dir_name}/text/{list1}', 'w') as text_file:
                text_file.write(s)
        except IndexError:
            print('Кажется документ пустой')

if __name__ == '__main__':
    main('atmosphere100')