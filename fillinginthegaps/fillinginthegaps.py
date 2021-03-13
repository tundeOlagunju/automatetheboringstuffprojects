#! python3

"""
fillinginthegaps.py - Finds all the files in a single given folder with a given prefix,
locates any gap in the numbering and rename all the later files to close the gap
"""
import os, re, shutil
from pathlib import Path


def format_number(number, number_group):
    for _ in range(len(number), len(number_group)):
        number = '0'+number
    return number

def fill_in_the_gaps(folder, prefix, extension):
    if not Path(folder).is_dir():
        print("Folder does not exist")
        return

    previous = 0
    file_pattern = re.compile(rf"(^{prefix})(\d+)({extension}$)")
    for prefix_file in sorted(os.listdir(folder)):
        mo = file_pattern.search(prefix_file)
        if mo == None:
            continue

        spam_group = mo.group(1)
        number_group = mo.group(2)
        extension_group = mo.group(3)

        expected_number = previous + 1
        actual_number = int(number_group)

        if actual_number != expected_number:
            correct_name = spam_group + format_number(str(expected_number),number_group) + extension_group
            print(f"Renaming file {prefix_file} to the correct value {correct_name} ...")
            shutil.move(prefix_file, correct_name)
            print(f'File renamed to {correct_name}')
            previous = expected_number
            continue

        previous = actual_number


fill_in_the_gaps(".", "spam", ".txt")