import os
import sys
import yaml
import django
import orders.models
from pprint import pprint

BASE_DIR = os.path.join(os.path.dirname((os.path.abspath(__file__))))


def read_yaml(file):
    try:
        with open(file, encoding='utf-8') as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)
    except Exception as e:
        print(f'ERROR!\n{e}')
    return data


def main():
    sys.path.append(os.path.join(BASE_DIR, 'test_project'))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    django.setup()

    file_list = os.listdir(os.path.join(BASE_DIR, 'data'))
    for file in file_list:
        data = read_yaml(os.path.join(BASE_DIR, 'data', file))
        # pprint(data)

    for model in orders.models:
        print(model)


if __name__ == '__main__':
    main()

