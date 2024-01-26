import csv
import os

import pandas as pd
import numpy as np

from mmconverter.params import ROW_OFFSET


def load_file(filename: str) -> list:
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ";")
        rows = [row for row in csv_reader]
    return rows


def check_filters(rows: list) -> int:
    if rows[1][0][:3] == "AXE":
        filters = 0
    else:
        filters = 1
    return filters


def find_row_levels(rows: list) -> list:
    filters = check_filters(rows)
    row_levels = [level for level in rows[filters + 1][0].split(",")]
    row_levels = [level.replace("AXE EN LIGNE :", "") for level in row_levels]
    row_levels = [level.strip(" * ").split() for level in row_levels]
    row_levels = [level[0] for level in row_levels[:-1]]
    return row_levels


def find_col_levels(rows: list) -> list:
    filters = check_filters(rows)
    col_levels = [level for level in rows[filters + 2][0].split(",")]
    col_levels = [level.replace("AXE EN COLONNE :", "") for level in col_levels]
    col_levels = [level.strip(" * ").split() for level in col_levels]
    col_levels = [level[0] for level in col_levels[:-1]]
    return col_levels


def find_col_names(rows: list, col_levels: list) -> dict:
    col_names = {}
    filters = check_filters(rows)
    for i, col in enumerate(col_levels):
        col_names[col] = []
        for el in rows[3+i+filters][1:-1]:
            if el:
                new_el = el
            col_names[col].append(new_el)
    return col_names


def get_data(rows: list, row_levels: list, col_levels: list, col_names: list) -> list:

    filters = check_filters(rows)

    data_rows = [row for row in rows[filters + 3 + len(col_levels) : -1]] #-1 car on enlève la mention Médiamétrie finale
    
    row_level_data = {row_level : "" for row_level in row_levels}
    col_level_data = {col_level : "" for col_level in col_levels}
    val_level_data = {"Valeur" : ""}

    all_rows = []

    for row in data_rows:
        
        # GETTING THE ROW LEVEL INFORMATION
        
        row_level = row[0]
        char = " "
        counter = 0
        
        while char == " ":
            char = row_level[counter]
            if char == " ":
                counter += 1
        
        row_level_index = counter // ROW_OFFSET
        row_level_data[row_levels[row_level_index]] = row_level.strip()
            
        if row_level_index == len(row_levels) - 1:
            
            for i, datapoint in enumerate(row[1:]):

                # GETTING THE COLUMN LEVEL INFORMATION
                for col in col_levels:
                    col_level_data[col] = col_names[col][i]

                # GETTING THE VALUE INFORMATION
                val_level_data["Valeur"] = datapoint
                
                #print(datapoint)
                
                new_row = {**row_level_data, **col_level_data, **val_level_data}
                all_rows.append(new_row)
    
    return all_rows


def get_df(data: list) -> pd.DataFrame:
    df = pd.DataFrame(data)
    return df


def process_rows(rows: list) -> pd.DataFrame:
    row_levels = find_row_levels(rows)
    col_levels = find_col_levels(rows)
    col_names = find_col_names(rows, col_levels)
    all_rows = get_data(rows, row_levels, col_levels, col_names)
    df = get_df(data = all_rows)
    return df


def export_csv(df: pd.DataFrame, filename: str):
    output_file = f"{filename[:-4]}_converted.csv"
    df.to_csv(output_file, sep = ";", index = False)
    