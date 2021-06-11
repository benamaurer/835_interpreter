era_file_name = '835test'
with open(era_file_name + '.txt', 'r') as file:
    data = file.read().replace('\n', '')
    print(data)