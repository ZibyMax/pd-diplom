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
        return None
    return data


def main():
    sys.path.append(os.path.join(BASE_DIR, 'getgoods'))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    django.setup()
    from orders.models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter

    file_list = os.listdir(os.path.join(BASE_DIR, 'data'))
    shop_counter = 0
    goods_counter = 0
    for file in file_list:
        shop_data = read_yaml(os.path.join(BASE_DIR, 'data', file))
        if shop_data is not None:
            shop_counter += 1
            goods_counter += len(shop_data['goods'])

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
            for item in shop_data['goods']:
                category = Category.objects.get(id=item['category'])
                name = item['model']
                product, created = Product.objects.get_or_create(name=name, category=category)

                product_info, created = ProductInfo.objects.get_or_create(
                    id=item['id'],
                    product=product,
                    name=item['name'],
                    price=item['price'],
                    price_rrc=item['price_rrc'],
                    quantity=item['quantity'],
                    shop=shop
                )

                for parameter_name, value in item['parameters'].items():
                    parameter, created = Parameter.objects.get_or_create(name=parameter_name)
                    product_parameter, created = ProductParameter.objects.get_or_create(
                        product_info=product_info,
                        parameter=parameter,
                        value=value
                    )

    print(f'Installed goods: {goods_counter} item(s) from {shop_counter} shop(s)')


if __name__ == '__main__':
    main()

