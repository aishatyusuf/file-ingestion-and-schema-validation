
import os
import logging
import subprocess
import yaml
import pandas as pd
import datetime
import gc
import re

#Reading the File

def read_config_file(filepath):
  with open (filepath, 'r') as stream:
    try:
      return yaml.safe_load(stream)
    except yaml.YAMLError as exc:
      logging.error(exc)

def replacer(string, char):
    """
    Replacing repeated characters with a single occurence
    """
    pattern = char + '{2,}'
    string = re.sub(pattern, char, string) 
    return string

def col_name_val(df, table_config):
    """
    Standardizing and validating column names of the dataframe 
    against the expected set of column names
    """
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace('[^\w]', '_', regex=True)
    df.columns = list(map(lambda x: x.strip('_'), list(df.columns)))
    df.columns = list(map(lambda x: replacer(x, '_'), list(df.columns)))

    expected_col = list(map(lambda x: x.lower(), table_config['columns']))
    expected_col.sort()
    df.columns = list(map(lambda x: x.lower(), list(df.columns)))
    df = df.reindex(sorted(df.columns), axis=1)

    if len(df.columns) == len(expected_col) and list(expected_col) == list(df.columns):
        print("Column name and length validation passed")
        return 1
    else:
       print("Column name and length validation failed")
       mismatched_columns_file = list(set(df.columns).difference(expected_col))
       print("The following file columns are not in the YAML file", mismatched_columns_file)
       missing_YAML_file = list(set(expected_col).difference(df.columns))
       print("The following YAML columns are not in the file uploaded", missing_YAML_file)
       logging.info(f'dataframe columns: {df.columns}')
       logging.info(f'expected columns: {expected_col}')
       return 0
