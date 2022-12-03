# coding=utf-8

import xlrd
import numpy as np

DATASETS = [
    {'workbook_path': 'sample.xlsx', 'sheet_name': 'For C8 between lines'}
]

def read_from_excel_file(workbook_path, sheet_name):
    book = xlrd.open_workbook(workbook_path)
    sheet = book.sheet_by_name(sheet_name)
    return [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]

def remove_rows(data):
    return data[1:]

def remove_columns(data):
    return [row[:2] for row in data]

def convert_to_floats_matrix(data):
    return [{'x': float(row[0]), 'y': float(row[1])} for row in data]

def average_by_x_coordinates(data):
    data_grouped_by_x_coordinates = {}
    for row in data:
        if not(row['x'] in data_grouped_by_x_coordinates.keys()): data_grouped_by_x_coordinates[row['x']] = []
        data_grouped_by_x_coordinates[row['x']].append(row['y'])
    return [{'x': x, 'y': 0 if len(y_values) == 0 else sum(y_values) / len(y_values)} for x, y_values in data_grouped_by_x_coordinates.items()]

def sort_by_x_coordinates(data):
    return sorted(data, key=lambda p: p['x'])

def calculate_current_vector(data, left_data_index):
    return {'from': data[left_data_index], 'to': data[left_data_index + 1]}

def calculate_y_coordinate(current_vector, x):
    f, t = current_vector['from'], current_vector['to']
    return f['y'] + (x - f['x']) * (t['y'] - f['y']) / (t['x'] - f['x'])

def fft(x):
    x = np.asarray(x, dtype=float)
    N = x.shape[0]

    if np.log2(N) % 1 > 0:
        raise ValueError("size of x must be a power of 2")

    N_min = min(N, 32)

    n = np.arange(N_min)
    k = n[:, None]
    M = np.exp(-2j * np.pi * n * k / N_min)
    X = np.dot(M, x.reshape((N_min, -1)))

    while X.shape[0] < N:
        X_even = X[:, :X.shape[1] / 2]
        X_odd = X[:, X.shape[1] / 2:]
        factor = np.exp(-1j * np.pi * np.arange(X.shape[0])
                        / X.shape[0])[:, None]
        X = np.vstack([X_even + factor * X_odd,
                       X_even - factor * X_odd])

    return X.ravel()

for dataset in DATASETS:
    data = read_from_excel_file(dataset['workbook_path'], dataset['sheet_name'])
    data = remove_rows(data)
    data = remove_columns(data)
    data = convert_to_floats_matrix(data)
    data = average_by_x_coordinates(data)
    data = sort_by_x_coordinates(data)

    min_x, min_y, max_x, max_y, points_count = data[0]['x'], data[0]['y'], data[-1]['x'], data[-1]['y'], len(data)

    y_matrix_size = 1
    while y_matrix_size < points_count:
        y_matrix_size *= 2

    y = []
    data_index = 0
    step = (max_x - min_x) / (y_matrix_size - 1)
    cv = calculate_current_vector(data, data_index)
    for y_matrix_index in range(y_matrix_size):
        cx = min_x + y_matrix_index * step
        if (data[data_index]['x'] >= min_x) and (data[data_index]['x'] <= max_x):
            while (data_index + 1 < points_count) and (data[data_index + 1]['x'] < cx):
                data_index += 1
        cv = calculate_current_vector(data, max(data_index, points_count - 2))
        cy = calculate_y_coordinate(cv, cx)
        print(cx, cy)
        y.append(cy)

    # result = fft(np.asarray(y))
    # print(result)
