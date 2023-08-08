#!/usr/bin/env python3

from os.path import exists, isfile, join
from os import mkdir, listdir, remove, rename
from datetime import date, timedelta, datetime

def read_file(file_name):
    """ Read a file """
    with open(file_name, 'r') as file:
        return file.read()
    
def write_file(file_name, content):
    """ Write a file """
    with open(file_name, 'w') as file:
        file.write(content)

def get_name(file_path):
    """ Get the name of a file """
    return file_path.split('/')[-1]

def remove_files_in_directory(directory_path):
    """ Remove all files in a directory """
    try:
        # Get a list of all files in the directory
        file_list = listdir(directory_path)

        # Iterate through the files and remove them one by one
        for filename in file_list:
            file_path = join(directory_path, filename)
            if isfile(file_path):
                remove(file_path)
    except OSError as e:
        print(f"Error: {e}")

def rename_file(file_path, new_name):
    """ Rename a file """
    try:
        new_file_path = join(file_path, new_name)
        rename(file_path, new_file_path)
    except OSError as e:
        print(f"Error: {e}")

def snake_case(string):
    """ Convert a string to snake case """
    if not isinstance(string,str):
        raise TypeError("Il faut aue ce soit une chaine de caractere")
    return string.lower().replace(' ', '_')

"""
:param day_of_week: The day of the week in integer format
"""
def get_week_timeframe(day_of_week):
    """ Return the timeframe for the next Friday """
    today = date.today()
    current_weekday = today.weekday()
    days_until_day_of_week = (day_of_week - current_weekday) % 7
    begin_date = today + timedelta(days=days_until_day_of_week - 7)
    end_date = begin_date + timedelta(days=6)
    return begin_date, end_date

#FIXME: This function is not working properly
def get_month_timeframe(year,month):
    """ Return the timeframe for a specific month """
    # set the first day of the month
    begin_date = date(year, month, 1)

    # set the last day of the month
    last_day_of_month = 31 if month == 12 else (date(year, month + 1, 1) - timedelta(days=1)).day
    end_date = date(year, month, last_day_of_month)

    return begin_date, end_date

#FIXME: This function is not working properly
def get_year_timeframe(year):
    """ Return the timeframe for a specific year """
    begin_date = date(year, 1, 1)
    end_date = date(year, 12, 31)

    return begin_date, end_date

""" verify if the settings.json file exists """
if not exists("cert_bulletin_gen/settings.json"):
    raise FileNotFoundError("Le fichier settings.json est introuvable")

""" verify if aout directory exists """
if not exists("cert_bulletin_gen/aout"):
    mkdir("cert_bulletin_gen/aout")