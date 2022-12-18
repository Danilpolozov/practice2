import sys
import argparse


def output_function(filename, output_string):
    if filename:
        with open(filename, 'a') as file1:
            file1.write(output_string + "\n")
    print(output_string)


def parse_csv(filename, country, year, output, total_year):
    head = None
    is_first_line = True
    with open(filename, "r") as file:
        first_10_medals = 0
        medals = 0
        country_exist = False
        olympics_held_this_year = False
        total_year_dict = dict()
        for line in file.readlines():
            data = line.strip().split(';')

            if is_first_line:
                head = data
                is_first_line = False
                continue
            if total_year:
                if total_year == data[head.index("Year")] and data[-1] != "NA":
                    if not data[head.index("Team")] in total_year_dict:
                        total_year_dict[data[head.index("Team")]] = {data[head.index("Medal")]: 1}
                    else:
                        if not data[head.index("Medal")] in total_year_dict[data[head.index("Team")]]:
                            total_year_dict[data[head.index("Team")]][data[head.index("Medal")]] = 1
                        else:
                            total_year_dict[data[head.index("Team")]][data[-1]] += 1
            if (country == data[head.index("NOC")] or country == data[head.index("Team")]):
                country_exist = True
            if year == data[head.index("Year")]:
                olympics_held_this_year = True
            if (country == data[head.index("NOC")] or country == data[head.index("Team")]) and year == data[
                head.index("Year")]:
                if first_10_medals < 10 and data[head.index("Medal")] != "NA":
                    output_function(output,
                                    f"Name: {data[head.index('Name')]} Sport: {data[head.index('Sport')]} Medal: {data[head.index('Medal')]}")
                    first_10_medals += 1
                if data[head.index("Medal")] != "NA":
                    medals += 1
        if not olympics_held_this_year:
            output_function(output, f"Олімпіада не проводилась {year} року")

        if not country_exist:
            output_function(output, f"Країна {country} не існує")
        if medals:
            output_function(output, "Загальна кількість медалей: " + str(medals))
        if not total_year_dict and total_year is not None:
            output_function(output, f"Тотальна кількість медалей у рік {total_year} не знайдена")
        elif total_year is None:
            pass
        else:
            total_year_output_string = ""
            for country in total_year_dict:
                total_year_output_string = total_year_output_string + country + " "
                for medal in total_year_dict[country]:
                    total_year_output_string = total_year_output_string + medal + ":" + str(total_year_dict[country][medal]) + " "
                total_year_output_string = total_year_output_string + "\n"
            output_function(output, total_year_output_string)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("-medals", nargs=2)
    parser.add_argument("-output", default=None)
    parser.add_argument("-total", default=None)
    arguments = parser.parse_args()
    filename = arguments.filename
    country = arguments.medals[0]
    year = arguments.medals[1]
    output = arguments.output
    total_year = arguments.total
    parse_csv(filename, country, year, output, total_year)


if __name__ == '__main__':
    main()
