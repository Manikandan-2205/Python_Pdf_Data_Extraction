import pdfplumber
import re
import pandas as pd


def start_end(data_list):
    start, end = [], []
    for ind, line in enumerate(data_list):
        if 'RELL_NO' in line and 'NAME' in line and 'PERCENTAGE_1' in line and 'PERCENTAGE_2' in line and 'PERCENTAGE_3' in line:
            # print(ind, line)
            start.append(ind)
        if 'Computer Systems Analyst – They design software and systems as per the' in line:
            # print(ind, line)
            end.append(ind)

    # print(start, end)
    return start, end


def main():
    lines = []
    pdf = pdfplumber.open('data.pdf')
    # print(pdf.pages[0].extract_text())
    for page in pdf.pages:
        # print(page.extract_text().splitlines())
        for line in page.extract_text().splitlines():
            # print(line)
            lines.append(re.sub('\s+', ' ', line.strip()))

    start, end = start_end(lines)

    if start == [] or end == []:
        print("Keywords Not Found!")
        return

    start, end = min(start), max(end)
    # print(start, end)
    # print(lines[start:end])

    result = {'RELL_NO': [], 'NAME': [], 'PERCENTAGE_1': [],
              'PERCENTAGE_2': [], 'PERCENTAGE_3': []}

    for data in lines[start:end]:
        # print(data.split())
        if 'RELL_NO' not in data and 'NAME' not in data and 'PERCENTAGE_1' not in data and 'PERCENTAGE_2' not in data and 'PERCENTAGE_3' not in data:
            result['RELL_NO'].append(data.split()[0])
            result['NAME'].append(''.join(data.split()[1:-3]))
            result['PERCENTAGE_1'].append(data.split()[-3])
            result['PERCENTAGE_2'].append(data.split()[-2])
            result['PERCENTAGE_3'].append(data.split()[-1])

    # print(result)

    df = pd.DataFrame(result)
    print(df)

    df.to_csv('result.csv', index=False)


main()
