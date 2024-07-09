from logging import Logger
from typing import Any, NamedTuple, Sequence, TypeAlias

import requests
from requests import RequestException

_StrKeysDict: TypeAlias = dict[str, Any]


class RestCountriesFieldNames(NamedTuple):
    # more fields can be found at
    # https://gitlab.com/restcountries/restcountries/-/blob/master/FIELDS.md
    NAME = 'name'
    CAPITAL = 'capital'
    FLAGS_AS_LINKS = 'flags'


class RestCountriesScraper:
    __BASE_URL = f'https://restcountries.com/v3.1/all'

    def __init__(
            self, logger: Logger, field_names_to_include: Sequence[str],
            include_only_png_flag_link: bool = True
    ):
        self.__logger = logger
        self.__field_names_to_include = field_names_to_include
        self.__include_only_png_flag_link = include_only_png_flag_link

    def get_data_for_chosen_fields(self) -> list[dict[str, str]]:
        raw_data = self.__query_data()
        cleaned_data = self.__clean_up_data(raw_data)
        return cleaned_data

    def __clean_up_data(self, countries_data: list[_StrKeysDict]) -> list[_StrKeysDict]:
        for specific_country_data in countries_data:
            self.__leave_single_capital(specific_country_data)
            self.__leave_only_official_name(specific_country_data)
            # this could be speed-optimized by having two methods, depending on whether
            # to include png flag only, but I left it this way for more clear code, as
            # it is just a test task. If it was a real one, I would check how much data goes
            # through this method and then would decide
            if self.__include_only_png_flag_link:
                self.__remove_svg_flag_link_and_rename_flags_key_to_flag_url(specific_country_data)
        return countries_data

    def __query_data(self) -> list[_StrKeysDict]:
        result = requests.get(self.__compose_url_with_fields_filters())
        try:
            result.raise_for_status()
        except RequestException as e:
            self.__logger.error('failed to make request', e)
            raise
        return result.json()

    def __remove_svg_flag_link_and_rename_flags_key_to_flag_url(self, country_data: _StrKeysDict):
        country_data['flag'] = country_data['flags']['png']
        country_data.pop('flags')

    def __leave_only_official_name(self, country_data: _StrKeysDict):
        country_data['name'] = country_data['name']['common']

    def __leave_single_capital(self, country_data: _StrKeysDict):
        """
        as very few countries has several capitals, leave only
        the first one to ensure keep data format consistent across countries
        """
        # some countries have no capital
        if country_data['capital']:
            country_data['capital'] = country_data['capital'][0]

    def __compose_filter_fields_url_part(self) -> str:
        return '?fields=' + ','.join(self.__field_names_to_include)

    def __compose_url_with_fields_filters(self) -> str:
        return self.__BASE_URL + self.__compose_filter_fields_url_part()
