# coding=utf-8

import xlrd
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack

DATASETS = [
    {'workbook_path': 'sample.xlsx', 'sheet_name': 'For C8 between lines'}
]

MAX_N = 1024

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

for dataset in DATASETS:
    data = read_from_excel_file(dataset['workbook_path'], dataset['sheet_name'])
    data = remove_rows(data)
    data = remove_columns(data)
    data = convert_to_floats_matrix(data)
    data = average_by_x_coordinates(data)
    data = sort_by_x_coordinates(data)

    min_x, max_x, points_count = data[0]['x'], data[-1]['x'], len(data)

    y_matrix_size = points_count

    y = []
    data_index = 0
    step = (max_x - min_x) / (y_matrix_size - 1)
    cv = calculate_current_vector(data, data_index)
    for y_matrix_index in range(y_matrix_size):
        cx = min_x + y_matrix_index * step
        if (data[data_index]['x'] >= min_x) and (data[data_index]['x'] <= max_x):
            while (data_index + 1 < points_count - 1) and (data[data_index + 1]['x'] < cx):
                data_index += 1
        cv = calculate_current_vector(data, data_index)
        cy = calculate_y_coordinate(cv, cx)
        y.append(cy)

    N = y_matrix_size
    T = 1.0 / N
    x = np.linspace(0.0, N * T, N)
    # y = np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(80.0 * 2.0*np.pi*x)
    x0 = np.linspace(0.0, 1.0 // (2.0 * T), N // 2)
    y0 = y
    yf = scipy.fftpack.fft(np.asarray(y))
    xf = np.linspace(0.0, 1.0 // (2.0 * T), N // 2)

    fig, ax = plt.subplots()
    ax.plot(x0, 2.0 / N * np.abs(y0[:N // 2]))
    plt.show()
    fig, ax = plt.subplots()
    ax.plot(xf, 2.0 / N * np.abs(yf[:N // 2]))
    plt.show()
