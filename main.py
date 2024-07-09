from logging import Logger

from make_table_to_print_from_data import make_table_to_print_from_data
from rest_countries_scraper import RestCountriesFieldNames, RestCountriesScraper

if __name__ == '__main__':
    logger = Logger(__name__)
    scraper = RestCountriesScraper(
        logger,
        field_names_to_include=(
            RestCountriesFieldNames.NAME,
            RestCountriesFieldNames.CAPITAL,
            RestCountriesFieldNames.FLAGS_AS_LINKS
        )
    )
    countries_data = scraper.get_data_for_chosen_fields()
    table = make_table_to_print_from_data(['name', 'capital', 'flag_link'], countries_data)
    print(table)
