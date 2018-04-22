import openpyxl
import requests

BASE_COLUMNS = {
    'value': 1,
    'expected_result': 2,
    'test_result': 3,
    'result': 4,
}

data_file = 'nom_tests_data.xlsx'
wb = openpyxl.load_workbook(data_file)
ws = wb.active

error_code = 'error'
bad_response_code = 'bad response'


def nominatim_reverse_geocoding(lat, lon):
    base_url = 'https://nominatim.openstreetmap.org/reverse?format=json&accept-language=en-US'
    url = f'{base_url}&lat={lat}&lon={lon}'
    try:
        return requests.get(url).json()
    except:
        return None


def save_value(result, row, col=BASE_COLUMNS['result']):
    ws.cell(row=row, column=col, value=result)
    wb.save(data_file)


def reverse_geocoding_test(value, expected_result, row):
    lat, lon = value.replace(' ', '').split(',')
    nominatim_result = nominatim_reverse_geocoding(lat, lon)

    if nominatim_result is None:
        save_value(None, row, BASE_COLUMNS['test_result'])
        save_value(bad_response_code, row)
        return

    if nominatim_result.get(error_code):
        save_value(error_code, row, BASE_COLUMNS['test_result'])
        result = 'done' if expected_result is not None and expected_result == error_code else error_code
        save_value(result, row)
        return

    display_name = nominatim_result['display_name']
    save_value(display_name, row, BASE_COLUMNS['test_result'])
    result = 'done' if expected_result is None or expected_result in display_name else error_code
    save_value(result, row)


row = 2

while True:
    test_value = ws.cell(row=row, column=BASE_COLUMNS['value']).value
    test_expected_result = ws.cell(row=row, column=BASE_COLUMNS['expected_result']).value
    if test_value is None:
        break

    if test_value.isdigit:
        reverse_geocoding_test(test_value, test_expected_result, row)
    row += 1
