import csv
from beeprint import pp

def csv_dict_conversion(dict_file):
    with open(dict_file, mode='r') as inp:
        reader = csv.reader(inp)
        dict = {rows[0]: rows[1] for rows in reader}
        return dict


if __name__ == '__main__':
    # print(str(csv_dict_conversion('csv_dict.csv')))
    pp(csv_dict_conversion('csv_dict.csv'))