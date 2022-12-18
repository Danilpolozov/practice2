import sys
import argparse


def output_function(filename, output_string):
    if filename:
        with open(filename, 'a') as file1:
            file1.write(output_string + "\n")
    print(output_string)


def interactive(filename):
    while True:
        country = input("Введіть назву країни або exit для виходу ")
        if country == "exit":
            break
        statistic_dict = dict()
        first_participate = ""
        first_participate_year = None
        is_first_line = True
        with open(filename, "r") as file:
            for line in file.readlines():
                data = line.strip().split(';')

                if is_first_line:
                    head = data
                    is_first_line = False
                    continue
                if first_participate_year is None:
                    first_participate_year = data[head.index("Year")]
                    first_participate = f"Перша участь у олімпіаді {data[head.index('Year')]} у {data[head.index('City')]}"
                if data[head.index("Team")].lower() == country.lower() and data[head.index("Medal")] != "NA":
                    if not data[head.index("Year")] in statistic_dict:
                        statistic_dict[data[head.index("Year")]] = {data[head.index("Medal")]: 1}
                    else:
                        if not data[head.index("Medal")] in statistic_dict[data[head.index("Year")]]:
                            statistic_dict[data[head.index("Year")]][data[head.index("Medal")]] = 1
                        else:
                            statistic_dict[data[head.index("Year")]][data[head.index("Medal")]] += 1


        print(first_participate)
        if not statistic_dict:
            print(f"Загальна кількість медалей по країнам {country} не знайдена")
        else:
            overall_output_string = ""
            min_medals = 9999
            min_medal_year = ""
            max_medals = 0
            max_medal_year = ""
            year_participate = 0
            total_medal_dict = dict()
            total_medals = 0
            for year in statistic_dict:
                year_participate += 1
                total_medal_year = 0
                for medal in statistic_dict[year]:
                    total_medal_year += statistic_dict[year][medal]
                    if medal not in total_medal_dict:
                        total_medal_dict[medal] = statistic_dict[year][medal]
                    else:
                        total_medal_dict[medal] += statistic_dict[year][medal]
                if total_medal_year > max_medals:
                    max_medals = statistic_dict[year][medal]
                    max_medal_year = year
                if total_medal_year < min_medals:
                    min_medals = statistic_dict[year][medal]
                    min_medal_year = year
                total_medals += total_medal_year
            print(f"Має найбільшу кількість медалей у {max_medal_year} році це {max_medals} медалей")
            print(f"Має найменшу кількість медалей у {min_medal_year} році це {min_medals} медалей")
            for medal in total_medal_dict:
                average_medals = total_medal_dict[medal] / year_participate
                average_medals = round(average_medals)
                print(f"В середньому отримує {average_medals} {medal} медалей")


def parse_csv(filename, country, year, output, total_year, overall):
    head = None
    is_first_line = True
    with open(filename, "r") as file:
        first_10_medals = 0
        medals = 0
        country_exist = False
        olympics_held_this_year = False
        total_year_dict = dict()
        overall_dict = dict()
        if overall:
            overall = set(overall)
        for line in file.readlines():
            data = line.strip().split(';')

            if is_first_line:
                head = data
                is_first_line = False
                continue
            if overall:
                if data[head.index("Team")] in overall and data[head.index("Medal")] != "NA":
                    if not data[head.index("Team")] in overall_dict:
                        overall_dict[data[head.index("Team")]] = {data[head.index("Year")]: 1}
                    else:
                        if not data[head.index("Year")] in overall_dict[data[head.index("Team")]]:
                            overall_dict[data[head.index("Team")]][data[head.index("Year")]] = 1
                        else:
                            overall_dict[data[head.index("Team")]][data[head.index("Year")]] += 1
            if total_year:
                if total_year == data[head.index("Year")] and data[head.index("Medal")] != "NA":
                    if not data[head.index("Team")] in total_year_dict:
                        total_year_dict[data[head.index("Team")]] = {data[head.index("Medal")]: 1}
                    else:
                        if not data[head.index("Medal")] in total_year_dict[data[head.index("Team")]]:
                            total_year_dict[data[head.index("Team")]][data[head.index("Medal")]] = 1
                        else:
                            total_year_dict[data[head.index("Team")]][data[head.index("Medal")]] += 1
            if country == data[head.index("NOC")] or country == data[head.index("Team")]:
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

        if not overall_dict and overall is not None:
            output_function(output, f"Загальна кількість медалей по країнам {overall} не знайдена")
        elif overall is None:
            pass
        else:
            overall_output_string = ""
            for country in overall_dict:
                max_medals = 0
                max_medal_year = ""
                for year in overall_dict[country]:
                    if overall_dict[country][year] > max_medals:
                        max_medals = overall_dict[country][year]
                        max_medal_year = year

                overall_output_string = overall_output_string+ f"{country} має найбільшу кількість медалей у {max_medal_year} році це {max_medals} медалей\n"
            output_function(output, overall_output_string)

        if not total_year_dict and total_year is not None:
            output_function(output, f"Тотальна кількість медалей у рік {total_year} не знайдена")
        elif total_year is None:
            pass
        else:
            total_year_output_string = ""
            for country in total_year_dict:
                total_year_output_string = total_year_output_string + country + " "
                for medal in total_year_dict[country]:
                    total_year_output_string = total_year_output_string + medal + ":" + str(
                        total_year_dict[country][medal]) + " "
                total_year_output_string = total_year_output_string + "\n"
            output_function(output, total_year_output_string)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("-medals", nargs=2)
    parser.add_argument("-output", default=None)
    parser.add_argument("-total", default=None)
    parser.add_argument("-overall", nargs="+", default=None)
    parser.add_argument("-interactive", action="store_true")
    arguments = parser.parse_args()

    filename = arguments.filename
    country = arguments.medals[0]
    year = arguments.medals[1]
    output = arguments.output
    total_year = arguments.total
    overall = arguments.overall
    parse_csv(filename, country, year, output, total_year, overall)
    if arguments.interactive:
        interactive(filename)


if __name__ == '__main__':
    main()
