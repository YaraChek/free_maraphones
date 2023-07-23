#!/usr/bin/python3

"""
The program makes a graph that reflects the number of IT vacancies in Ukraine.
The data is taken from the https://uadata.net.
"""

import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def game_over():
    """Completion of the program"""
    print("\nEnd of requests")
    exit()


def input_city(work_list):
    """
    Checking the correctness of entering the city number.
    :param work_list: list of cities available for processing
    :return: correct number
    """
    while True:
        number = input("\nОберіть, будь ласка, по якому місту Вам надати інформацію -\n"
                       "вводьте цифру та натискайте <Enter>.\n"
                       "Для того, щоб перейти до вибору інших міст зі списку, потрібно буде "
                       "закрити віконце з поточним графіком.\n")
        if number not in work_list:
            print("\nУВАГА: Неправильний ввод.\nОберіть, будь ласка, цифру зі списку.")
            continue
        else:
            return number


def numbers_to_analyze(number, list_dimension):
    """
    Checking the correctness of entering the number of cities.
    :param number: number of cities (or cities + country) for information processing
    :param list_dimension: total cities available for information processing
    :return: number of cities for information processing
    """
    while True:
        try:
            number = int(number)
            if number <= 0:
                print("\nВи ввели нуль або від'ємне число, тому програма припиняється.")
                game_over()
            elif number < list_dimension:
                return number
            else:
                print("\nВ нашому списку немає стільки міст. Навіть, якщо Україну приплюсувати.\n"
                      "Спробуйте ще раз.")
                number = input("\nПо скількох містах надати інформацію?\nІнформацію по Україні "
                               "вцілому також можна включити у видачу. Врахуйте це. ")
        except ValueError:
            print("\nТе, що Ви ввели - не є цілим числом. Будь ласка: ще раз.")
            number = input("\nПо скількох містах надати інформацію?\nІнформацію по Україні "
                           "вцілому також можна включити у видачу. Врахуйте це. ")


def main():
    UKRAINE_JSON = "https://uadata.net/work-positions/cities.json"
    city_list = {"0": "Україна в цілому",
                 "1": "Київ",
                 "2": "Одеса",
                 "3": "Львів",
                 "4": "Дніпро",
                 "5": "Харків",
                 "6": "Запоріжжя",
                 "7": "Тернопіль",
                 "8": "Кривий Ріг",
                 "9": "Завершити програму"}

    city_list_dimension = len(city_list)

    print("\nПрограма будує графік, що відображає кількість вакансій на IT-ринку в Україні.\n\n"
          "Дані беруться з ресурсу https://uadata.net.\n\n"
          "Інформація доступна, нажаль, лише по містах, що зазначені нижче.")

    while True:
        city = ""
        json_link = UKRAINE_JSON
        print()
        for k, v in city_list.items():
            print(": ".join((k, v)))
        n = numbers_to_analyze(
            input("\nПо скількох містах надати інформацію?\nІнформацію по Україні "
                  "вцілому також можна включити у видачу. Врахуйте це. "),
            city_list_dimension)

        # makes graph
        fig, axs = plt.subplots()
        cities_in_process = set()  # to avoid duplication of cities on the graph
        cities_in_process.clear()
        for i in range(n):
            answer = input_city(city_list)
            if answer not in cities_in_process:
                cities_in_process.add(answer)
                if answer == "9":
                    game_over()
                elif answer != "0":
                    city = city_list[answer]
                    json_link = "".join((UKRAINE_JSON, "?o=", city))
                else:
                    json_link = UKRAINE_JSON

                response = requests.get(json_link)
                data_json = response.json()
                df = pd.DataFrame(data_json["data"])
                df["at"] = pd.to_datetime(df["at"])

                df = df.rename(columns={"at": "Дата", "val": "Вакансії"})
                df.set_index('Дата', inplace=True)
                df["Вакансії"] = df["Вакансії"].replace(0, np.NaN)
                df["Вакансії"] = df["Вакансії"].interpolate()

                df["rolling_mean"] = \
                    df["Вакансії"].rolling(window=7).mean()

                axs.plot(df.index, df["rolling_mean"],
                         label="Україна" if json_link == UKRAINE_JSON else city)

        plt.title('Кількість вакансій по Україні')
        plt.xlabel("Дата", color='midnightblue')
        plt.ylabel("Вакансії", color='midnightblue')
        plt.ylim(bottom=0)  # makes graph from zero
        plt.legend()
        plt.show()


if __name__ == "__main__":
    main()
