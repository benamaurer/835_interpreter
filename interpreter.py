import csv
import pandas as pd
from beeprint import pp
from csv_info_to_dict import csv_dict_conversion


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


df_835_raw = pd.DataFrame(columns=['loop_ID', 'segment_ID', 'data_element_ID', 'data_element_value'])

loop_ids = ['none','1000A','1000B','2000','2100','2110','none']
loop_initiators = ['N1','LX','CLP','SVC','PLB']
# loop_ids = {'1000A':'N1','1000B':'N1','2000':'LX','2100':'CLP','2110':'SVC','none':'PLB'}
era_params_file_name = '835segments.csv'
debug_mode = False


dict_loops = csv_dict_conversion('loops.csv')
dict_segments = csv_dict_conversion('segments.csv')
dict_segment_ids = csv_dict_conversion('segment_ids.csv')


# DEPRECATED: replaced by the above dicts
# #import of 835 code table
# def era_table_import():
#     try:
#         with open(era_params_file_name, mode='r') as infile:
#             reader = csv.reader(infile)
#             with open(era_params_file_name, mode='w') as outfile:
#                 writer = csv.writer(outfile)
#                 era_codes = {rows[0]:rows[1] for rows in reader}
#
#         return era_codes
#     except Exception as e:
#         return f"Unable to access era parameters file. Error code: {e}"


def era_file_to_str(era_file_name):
    try:
        with open(era_file_name, 'r') as file:
            era_string = file.read().replace('\n', '')
        return era_string
    except:
        return 'Unable to find/convert era file.'


def era_decode(era_codes, era_string):

    segments = era_string.split('~')

    loop_number = 0

    for segment in segments:
        segment_name = str(segment.split('*')[0])
        segment_values = segment.split('*')[1:]
        if segment_name in loop_initiators:
            loop_number = loop_number + 1
        loop_id = loop_ids[loop_number]
        if debug_mode == True:
            print(segment_name)
        segment_value_id = 1
        for segment_value in segment_values:
            if debug_mode == True:
                if len(str(segment_value_id)) < 2:
                    print('    ' + segment_name + '0' + str(segment_value_id) + '  |  ' + str(segment_value))
                else:
                    print('    ' + segment_name + str(segment_value_id) + '  |  ' + str(segment_value))
            if segment_value == '':
                continue
            if len(str(segment_value_id)) < 2:
                df_835_raw.loc[len(df_835_raw.index)] = [str(loop_id), str(segment_name),'0' + str(segment_value_id),str(segment_value)]
            else:
                df_835_raw.loc[len(df_835_raw.index)] = [str(loop_id), str(segment_name),str(segment_value_id), str(segment_value)]
            segment_value_id = segment_value_id + 1

    return df_835_raw


def era_translate(era_df,era_code_dicts=[]):
    df_835_translated = pd.DataFrame(columns=['segment_category', 'segment_name','segment_value'])
    for index, row in era_df.iterrows():
        translated_segment = dict_segments.get(str(row['segment_ID']))
        translated_segment_ID = dict_segment_ids.get(str(row['segment_ID']) + str(row['data_element_ID']))
        df_835_translated.loc[len(df_835_translated.index)] = [translated_segment,translated_segment_ID,str(row['data_element_value'])]
        print()
    return df_835_translated


if __name__ == '__main__':
    raw_835 = era_decode('',era_file_to_str('835test.txt'))
    print(raw_835)
    print(era_translate(raw_835,era_code_dicts=[dict_segments,dict_segment_ids]))
    # pp(dict_loops)
    # pp(dict_segments)
    # pp(dict_segment_ids)