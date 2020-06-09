from AdsParser import Parser, Ad

def test():
    parser = Parser(buy='snyat', price_max='100000',
                    metro='Крестьянская застава')
    print(parser.form_request_yandex())

    parser.configure(city='moskva', buy='снять',
        house_type='kvartira', price_min='10000',
        price_max='100000', metro='Фрунзенская')

    print("Входные данные: \n{:s}\n{:s}\n{:s}\n{:s}\n{:s}\n{:s}\n".format(
          parser.city, parser.buy, parser.house_type, parser.price_min,
          parser.price_max, parser.metro))

    print("Запрос: {:s}\n".format(parser.form_request_yandex()))

    parser.page_init_yandex(100)
    print("Объявления: \n")

    for k in range(100):
        i = parser.get_ad_yandex(k)
        print('--', k, '--')
        print(i.url, i.title, i.address, i.price,
              sep='\n', end='\n\n\n')

test()
