#!/usr/bin/python3

from random import randint


def read_city(filename):
    with open(filename, 'r', encoding='utf-8') as inf:
        work_list = {line.strip() for line in inf}
    return work_list


def manual_input(to_exit, set_1, set_2):
    city_in = input()
    if city_in.upper() in to_exit:
        print('\nДякую за гру!\nТепер ви краще знаєте міста України.')
        exit()
    elif city_in == "":
        return manual_input(to_exit, set_1, set_2)
    elif city_in not in set_1 | set_2:
        print('Такого міста немає в базі даних')
        return manual_input(to_exit, set_1, set_2)
    else:
        return city_in


def check_1st_letter_exist(city_name, letters):
    while True:
        if city_name[-1].upper() in letters:
            return city_name[-1].upper()
        else:
            print(f'Міста, назва якого починається з "{city_name[-1].upper()}", в базі даних немає.'
                  f'\nТому спробуємо знайти місто, назва якого починається з попередньої букви, а '
                  f'саме "{city_name[-2].upper()}"')
            city_name = city_name[:-1]


TO_EXIT = {'STOP', 'EXIT', 'СТОП', 'ВИХІД', 'ДОСИТЬ', 'ДОСТАТНЬО'}
FILE_NAME = 'cities.dat'
cities = read_city(FILE_NAME)
cities_capital = {city.upper() for city in cities}
first_letters = {city[0].upper() for city in cities}
letter_city = {first_letter: tuple(city for city in cities if city[0] == first_letter)
               for first_letter in first_letters}
first_letters.clear()

print('Програма реалізує класичну гру "Міста".\n'
      'Перший гравець пише місто. На ту букву, на яку воно закінчується, другий гравець пише '
      'своє. І так - по колу.\n'
      'Міст не дуже багато (тільки Україна), тому повторюватися - можуть.\n\n'
      'Для того, щоб завершити гру, введіть: "Stop", "Exit", "Вихід", "Стоп", "Досить" або '
      '"Достатньо".\n\nПочинайте. Ви - гравець № 1.\nОтже, Ваше місто:')

player_1_city = manual_input(TO_EXIT, cities, cities_capital)
player_2_city = None
while True:
    if player_2_city is not None:
        last_letter = check_1st_letter_exist(player_2_city, letter_city)
        player_1_city = manual_input(TO_EXIT, cities, cities_capital)
        while player_1_city[0] != last_letter:
            print(f'Ні, не так. Ваше місто має починатися на літеру "{last_letter.upper()}"\n'
                  f'Пригадайте таке.')
            player_1_city = manual_input(TO_EXIT, cities, cities_capital)

    last_letter = check_1st_letter_exist(player_1_city, letter_city)
    player_2_city = letter_city[last_letter][randint(0, len(letter_city[last_letter]) - 1)]
    print(f'\nМоє місто: {player_2_city}\n')
