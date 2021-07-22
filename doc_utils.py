from ast import literal_eval
from typing import Text

import numpy as np
import pandas as pd


def _source_code_latex_matrix_to_np_array(mat_str):
    lines = mat_str.split('\\')
    arr = []
    for line in lines:
        line = line.replace(' ', '').strip('\n').split('&')
        if line == ['']:
            continue
        for i, x in enumerate(line):
            line[i] = float(x)
        arr.append(line)
    return np.array(arr)


def _pdf_latex_matrix_to_np_array(mat_str, num_cols):
    assert isinstance(num_cols, int) and num_cols > 0
    mat_str = ' '.join(mat_str.split()) # multiple whitespace --> single whitespacee
    individual_elems = mat_str.split()
    row = []
    count = 0
    mat = []
    for i, elem in enumerate(individual_elems):
        if i + 1 % num_cols == 0:
            mat.append(row)
            row = []
            count = 0
        row.append(float(elem))
    return mat


def latex_matrix_to_np_array(mat_str, num_cols=None, from_source=True):
    if from_source:
        return _source_code_latex_matrix_to_np_array(mat_str)
    else:
        return _pdf_latex_matrix_to_np_array(mat_str, num_cols)


def np_array_to_latex_matrix(arr, already_in_math_mode=False):
    if not already_in_math_mode:
        mat_str = '\['
    else:
        mat_str = ''
    mat_str += '\\begin{bmatrix}\n'
    for row in arr:
        temp_str = ''
        for elem in row:
            temp_str += str(elem) + ' & '
        temp_str = temp_str[0: -2] + '\\\\\n'
        mat_str += temp_str
        
    mat_str += '\\end{bmatrix}'
    if not already_in_math_mode:
        mat_str += '\]'
    return mat_str


def pandas_df_to_latex_table(df):
    cols = [str(df.index.name)] + [str(x) for x in df.columns]
    print(cols)
    n_cols = len(cols)

    table_str = ''

    table_str += '\\begin{center}\n'
    table_str += '\\begin{tabular}{||' + 'c|' * (n_cols + 1) + '|}\n'
    table_str += '\hline\n'
    table_str += ' & '.join(cols) + '\\\\\n'
    table_str += '\hline\hline\n'
    for row in df.itertuples():
        print(np.array(row).astype(str))
        table_str += ' & '.join(np.array(row).astype(str)) + '\\\\\n'
        table_str += '\hline\n'

    table_str += '\\end{tabular}\n'
    table_str += '\\end{center}'

    return table_str
