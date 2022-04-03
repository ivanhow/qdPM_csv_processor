import pandas
from openpyxl.workbook import Workbook


# Returns qc time int from list from QC Time column
def qc_time(qc_time_column: str):
    for i in qc_time_column:
        if i == '-' or i == ' ':
            str_list = qc_time_column.split(i)
            try:
                return int(str_list[0])
            except:
                return 0


# qdPM data to data frame
data_qdpm = pandas.read_csv('tasks_april.csv', sep=';')
print(data_qdpm)

# operators data to data frame and dictionary
data_operators = pandas.read_csv('operator_list.csv', sep=';')
operators_dict = data_operators.to_dict()

# operators names and nicks combined in dictionary also as lists
operators_names = operators_dict['dtp_name']
operators_names_list = list(operators_names.values())
operators_nicks = operators_dict['qdPM_nick']
operators_nicks_list = list(operators_nicks.values())
operators = {}
for key, value in operators_names.items():
    if key in operators_nicks:
        operators.update({value: operators_nicks[key]})

tasks_list = ['A01', 'CORR', 'QC', 'REP', 'INC', 'FD', 'IMD', 'OTHER']

result_numbers = dict((o, dict((t, 0) for t in tasks_list)) for o in operators_names_list)
result_time = dict((o, dict((t, 0) for t in tasks_list)) for o in operators_names_list)

artwork_pia = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'AM01',
               'HI01', 'HI0X', 'PS01', 'PS0X']
repro = ['R01', 'R02', 'R03']
inc = ['INC01', 'INC0X']
imd = ['IMDev']
fd = ['DD', 'FD']
for key, value in operators.items():
    for (index, row) in data_qdpm.iterrows():
        # Valid 'Assigned To', Nan in 'QC Time', operator in 'Assigned To' only
        if type(row['Assigned To']) == str and pandas.isna(row['QC Time']) and key in row['Assigned To']:
            if row['Type'] in artwork_pia:
                if row['Type'] in ['A01', 'HI01', 'PS01']:
                    # Increases the 'A01' number and time
                    result_numbers[key]['A01'] += 1
                    try:
                        result_time[key]['A01'] += int(row['Est. Time'])
                    except:
                        result_time[key]['A01'] += 0
                else:
                    # Increases the 'CORR' number and time
                    result_numbers[key]['CORR'] += 1
                    try:
                        result_time[key]['CORR'] += int(row['Est. Time'])
                    except:
                        result_time[key]['CORR'] += 0
            elif row['Type'] in repro:
                result_numbers[key]['REP'] += 1
                try:
                    result_time[key]['REP'] += int(row['Est. Time'])
                except:
                    result_time[key]['REP'] += 0
            elif row['Type'] in inc:
                result_numbers[key]['INC'] += 1
                try:
                    result_time[key]['INC'] += int(row['Est. Time'])
                except:
                    result_time[key]['INC'] += 0
            elif row['Type'] in imd:
                result_numbers[key]['IMD'] += 1
                try:
                    result_time[key]['IMD'] += int(row['Est. Time'])
                except:
                    result_time[key]['IMD'] += 0
            elif row['Type'] in fd:
                result_numbers[key]['FD'] += 1
                try:
                    result_time[key]['FD'] += int(row['Est. Time'])
                except:
                    result_time[key]['FD'] += 0
            elif row['Type'] not in fd or imd or inc or repro or artwork_pia:
                result_numbers[key]['OTHER'] += 1
                try:
                    result_time[key]['OTHER'] += int(row['Est. Time'])
                except:
                    result_time[key]['OTHER'] += 0
        # Valid 'Assigned To', valid 'QC Time', operator in 'Assigned To' and initials in 'QC Time'
        elif type(row['Assigned To']) == str and not pandas.isna(row['QC Time']) and key in row['Assigned To'] \
                and value in row['QC Time']:
            if row['Type'] in artwork_pia or repro or inc or imd or fd:
                # Increases the 'QC' number and time
                result_numbers[key]['QC'] += 1
                result_time[key]['QC'] += qc_time(row['QC Time'])
        # Valid 'Assigned To', valid 'QC Time', operator in 'Assigned To' and initials not in 'QC Time'
        elif type(row['Assigned To']) == str and not pandas.isna(row['QC Time']) and key in row['Assigned To'] \
                and value not in row['QC Time']:
            if row['Type'] in artwork_pia:
                if row['Type'] in ['A01', 'HI01', 'PS01']:
                    # Increases the 'A01' number and time
                    result_numbers[key]['A01'] += 1
                    try:
                        result_time[key]['A01'] += int(row['Est. Time'])
                    except:
                        result_time[key]['A01'] += 0
                else:
                    # Increases the 'CORR' number and time
                    result_numbers[key]['CORR'] += 1
                    try:
                        result_time[key]['CORR'] += int(row['Est. Time'])
                    except:
                        result_time[key]['CORR'] += 0
            elif row['Type'] in repro:
                # Increases the 'REP' number and time
                result_numbers[key]['REP'] += 1
                try:
                    result_time[key]['REP'] += int(row['Est. Time'])
                except:
                    result_time[key]['REP'] += 0
            elif row['Type'] in inc:
                # Increases the 'INC' number and time
                result_numbers[key]['INC'] += 1
                try:
                    result_time[key]['INC'] += int(row['Est. Time'])
                except:
                    result_time[key]['INC'] += 0
            elif row['Type'] in imd:
                # Increases the 'IMD' number and time
                result_numbers[key]['IMD'] += 1
                try:
                    result_time[key]['IMD'] += int(row['Est. Time'])
                except:
                    result_time[key]['IMD'] += 0
            elif row['Type'] in fd:
                # Increases the 'FD' number and time
                result_numbers[key]['FD'] += 1
                try:
                    result_time[key]['FD'] += int(row['Est. Time'])
                except:
                    result_time[key]['FD'] += 0

print(result_numbers)
print(result_time)

result_numbers_file = pandas.DataFrame(result_numbers)
result_numbers_file.to_excel('result_numbers_file.xlsx')
result_time_file = pandas.DataFrame(result_time)
result_time_file.to_excel('result_time_file.xlsx')