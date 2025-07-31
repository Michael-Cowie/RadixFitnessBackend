import requests
from configurations.django_config_parser import django_configs

FOODDATA_CENTRAL_API_KEY = django_configs.get("FoodData Central", "FOODDATA_CENTRAL_API_KEY")

NUMBER_OF_FOODS_TO_RETURN = 20


class FoodDataCentralService:
    """
    Service class to make API request to the FoodData Central API for nutritional
    information and reformat it into our desired format.

    Helpful documentation include,
        - https://fdc.nal.usda.gov/faq.html
        - https://fdc.nal.usda.gov/portal-data/external/dataDictionary
        - https://fdc.nal.usda.gov/download-datasets.html
    """

    BASE_URL = "https://api.nal.usda.gov/fdc/v1/foods"

    @staticmethod
    def get_foods_by_query_name(query):
        """
        The FoodData Central API offers five types of food groups,

        - Foundation Foods
        - SR Legacy
        - Food and Nutrient Database for Dietary Studies 2019-2020 (FNDDS 2019-2020)
        - Experimental Foods
        - Branded Foods
        """
        url = f"{ FoodDataCentralService.BASE_URL }/search"
        params = {
            "query": query,
            "api_key": FOODDATA_CENTRAL_API_KEY,
            "dataType": ["SR Legacy"],
            "pageSize": NUMBER_OF_FOODS_TO_RETURN,
            "pageNumber": 1,
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get("foods", [])
