import csv
import pandas as pd


# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_colwidth', None)


loop_ids = {'1000A':'N','1000B':'N','2000':'LX','2100':'CLP','2110':'SVC','none':'PLB'}
era_params_file_name = '835segments.csv'
debug_mode = False

#import of 835 code table
def era_table_import():
    try:
        with open(era_params_file_name + '.csv', mode='r') as infile:
            reader = csv.reader(infile)
            with open(era_params_file_name + '.csv', mode='w') as outfile:
                writer = csv.writer(outfile)
                era_codes = {rows[0]:rows[1] for rows in reader}
                
        return era_codes
    except Exception as e:
        return f"Unable to access era parameters file. Error code: {e}"


def era_file_to_str(era_file_name):
    try:
        with open(era_file_name, 'r') as file:
            era_string = file.read().replace('\n', '')
        return era_string
    except:
        return 'Unable to find/convert era file.'


def era_translate(era_codes, era_string):

    segments = era_string.split('~')

    df = pd.DataFrame(columns=['segment_ID','data_element_ID','data_element_value'])

    for segment in segments:
        segment_name = str(segment.split('*')[0])
        segment_values = segment.split('*')[1:]
        if debug_mode == True:
            print(segment_name)
        segment_value_id = 1
        for segment_value in segment_values:
            if debug_mode == True:
                if len(str(segment_value_id)) < 2:
                    print('    ' + segment_name + '0' + str(segment_value_id) + '  |  ' + str(segment_value))
                else:
                    print('    ' + segment_name + str(segment_value_id) + '  |  ' + str(segment_value))
            if len(str(segment_value_id)) < 2:
                df.loc[len(df.index)] = [str(segment_name),'0' + str(segment_value_id),str(segment_value)]
            else:
                df.loc[len(df.index)] = [str(segment_name),str(segment_value_id), str(segment_value)]
            segment_value_id = segment_value_id + 1

    return df









if __name__ == '__main__':
    print(era_translate('',era_file_to_str('835test.txt')))
