# coding=utf-8

import xlrd
import numpy as np

def read_from_excel_file(Workbook_path, sheet_name):
    book = xlrd.open_workbook(Workbook_path)
    sheet = book.sheet_by_name(sheet_name)
    return [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]

def remove_rows(data):
    return data[1:]

def remove_columns(data):
    return list(map(lambda row: {'x': row[0], 'y': row[1]}, data))

def average_by_x_coordinates(data):
    data_grouped_by_x_coordinates = {x: [] for x in data.keys()}
    for x, y in data:
        data_grouped_by_x_coordinates[x].append(y)
    return {x: 0 if len(y_values) == 0 else sum(y_values) / len(y_values) for x, y_values in data.values()}

def sort_by_x_coordinates(data):
    return sorted(data, key=lambda d: d['x'])

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

data = read_from_excel_file('sample.xlsx', 'For C8 between lines')
data = remove_rows(data)
data = remove_columns(data)
data = average_by_x_coordinates(data)
data = sort_by_x_coordinates(data)

x_coordinates = list(map(lambda p: p['x'], data))
min_x, max_x, points_count = min(x_coordinates), max(x_coordinates), len(x_coordinates)
print(min_x, max_x, points_count)

y = [p['y'] for p in data]

result = fft(np.asarray(y))
print(result)
