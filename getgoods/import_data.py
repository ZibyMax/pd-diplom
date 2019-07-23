import os
import sys
import yaml
import django


BASE_DIR = os.path.join(os.path.dirname((os.path.abspath(__file__))))


def read_yaml(file):
    try:
        with open(file, encoding='utf-8') as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)
    except Exception as e:
        print(f'ERROR!\n{e}')
    return data


def main():
    sys.path.append(os.path.join(BASE_DIR, 'getgoods'))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    django.setup()
    from orders.models import Shop, Category, Product, ProductInfo, Parameter,\
        ProductParameter, Order, OrderItem, Contact

    file_list = os.listdir(os.path.join(BASE_DIR, 'data'))
    for file in file_list:
        shop_data = read_yaml(os.path.join(BASE_DIR, 'data', file))

        # import shop.name
        shop, created = Shop.objects.update_or_create(name=shop_data['shop'])

        # import categories
        for category_data in shop_data['categories']:
            category, created = Category.objects.update_or_create(
                id=category_data['id'],
                name=category_data['name'],
            )
            category.shops.add(shop)

        # import goods


if __name__ == '__main__':
    main()

