from tabulate import tabulate

from typehints import StrKeysDict


def make_table_to_print_from_data(headers: list[str], data: list[StrKeysDict]) -> str:
    rows = [[item[column] for column in headers] for item in data]
    return tabulate(rows, headers, tablefmt='grid')
