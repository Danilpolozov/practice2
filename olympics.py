import sys


def task1(filename, country, year, output):
    head = None
    is_first_line = True
    with open(filename, "r") as file:

        for line in file.readlines():
            line = line.replace('"', "")
            data = line.strip().split(",")

            if is_first_line:
                head = data
                is_first_line = False
                continue

            if (country == data[head.index("NOC")] or country == data[head.index("Team")]) and year == data[
                head.index("Year")]:
                pass



def task2():
    pass


def main():
    args = sys.argv
    if args[2] == "-medals":
        filename = args[1]
        country = args[3]
        year = args[4]
        print("OK")
        try:
            output = args[args.index("-output")]
        except:
            output = None
        task1(filename, country, year, output)


if __name__ == '__main__':
    main()
