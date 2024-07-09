from logging import Logger

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
    result = scraper.get_data_for_chosen_fields()
    print(result)
