from rest_framework import serializers


class FoodSearchResultSerializer(serializers.Serializer):
    description = serializers.SerializerMethodField()
    calories = serializers.SerializerMethodField()
    protein = serializers.SerializerMethodField()
    fat = serializers.SerializerMethodField()
    carbs = serializers.SerializerMethodField()

    def get_nutrient_info(self, food_nutrients, nutrient_name):
        for nutrient in food_nutrients:
            if nutrient["nutrientName"] == nutrient_name:
                return {"value": nutrient["value"], "unit": nutrient["unitName"]}
        return None

    def get_description(self, food):
        return food["description"]

    def get_calories(self, food):
        """
        The FoodData Central API returns multiple variations of Energy,

        - Energy (Atwater General Factors)
        - Energy (Atwater Specific Factors)
        - Energy - with unit_name = "KCAL"
        - Energy - with unit_name = "kJ"

        However, the SR Legacy food only returns "Energy". However, the unit_name
        needs to be inspected to determine if the unit is "KCAL" or "kJ".
        """

        def _kj_to_kcal(info):
            if info["unit"] == "kJ":
                info["unit"] = "KCAL"
                info["value"] = round(info["value"] / 4.18, 2)
            return info

        return _kj_to_kcal(self.get_nutrient_info(food["foodNutrients"], "Energy"))

    def get_protein(self, food):
        return self.get_nutrient_info(food["foodNutrients"], "Protein")

    def get_fat(self, food):
        """
        The FoodData Central API returns multiple variations of fats,

        - Fatty acids, total monounsaturated =  Monounsaturated fats are a type of unsaturated
          fat that have one double bond in their fatty acid chain. Monounsaturated fats are
          considered heart-healthy and can help reduce bad cholesterol levels (LDL) while
          maintaining or even increasing good cholestrol levels (HDL)

          Examples: Olive oil, avocados and nuts such as almonds and peanuts.

        - Fatty acids, total polyunsaturated = Polyunsaturated fats are another type of unsaturated,
          but unlike monounsaturated fats, they have more than one double bond in their fatty acid
          chain. This includes fatty acids which is also heart healthy.

          Examples: Omega-3 and Omega-6 acids, found in fish, flaxseeds, walnuts and certain
                    vegetable oils (sunflower, corn oil, etc...).

        - Fatty acids, total saturated = Saturated fats are fats where all bonds between
          carbon atoms are single bonds. They are "saturated" with hydrogen atoms, meaning
          every carbon atom is fully surrounded by hydrogen. Typically, solid at room
          temperature and high intake can raise LDL (bad) cholesterol, increasing heart
          disease risk.

          Examples: Butter, cheese, red meat and coconut oil.

        - Fatty acids, total trans = These are unsaturated fats, but their chemical structure
          has been altered (usually by processing), so they act more like saturated fats. The
          "trans" refers to the specific arrangement of hydrogen atoms across the double
          bond in the fatty acid chain. Trans fats are harmful because they can raise LDL (bad)
          cholesterol and lower HDL (good) cholesterol, increasing the risk of heart disease.

          Examples: Fried foods and baked good made with partially hydrogenated oils.

        - Fatty acids, total trans-polyenoic = This is a subtype of trans fats where the fat
          molecules have more than one double bond in its structure, but these bonds are in the
          "trans" configuration. The "trans" configuration refers to the specific arrangement
          of hydrogen atoms around a carbon-carbon double bond in a fatty acid molecule. Like
          other trans fats, these are harmful to heart health, increasing the risk of heart disease.

          Examples: Rare in natural foods, but can be found in some processed foods that contain
                    partially hydrogenated oils (hydrogenated oils is made by forcing hydrogen
                    gas into oil at high pressure).

        - Fatty acids, total trans-monoenoic = Another type of trans fats, but in this case,
          the fat molecule has only one double bond, and it is in the "trans" configuration.
          This is also harmful, contributing to increased risk of heart disease by negatively
          affecting cholesterol levels.

          Examples: Found in small amount in some animal products and in larger amounts in
                    processed foods made with partially hydrogenated oils.

        - Total lipid (fat) = The sum of all fats in the food, including both healthy and
          potentially harmful fats.

        For the purpose of my API, I will be using "Total lipd (fat)" to only track
        the sum of all fats.
        """
        return self.get_nutrient_info(food["foodNutrients"], "Total lipid (fat)")

    def get_carbs(self, food):
        """
        The FoodData Central API returns multiple variations of carbohydrates,

        - Carbohydrate, by difference
        - Carbohydrates
        - Carbohydrate, by summation
        - Carbohydrate, other

        However, the SR Legacy data will always use "Carbohydrate, by difference".

        Here, "Carbohydrate, by difference" is a method used to estimate the total
        amount of carbohydrates in a food product. It is called "by difference" because
        it is calculated indirectly by subtracting the other known components of the food
        such as protein, fat, moisture and ash from the total weight of the food.

        Carbohydrate, by difference = Total Weight of Food - (Protein + Fat + Moisture + Ash)

        Directly measuring carbohydrates in food is often more complex and less precise than
        measuring other components like protein or fat. The "by difference" method offers a
        practical and reasonably accurate way to estimate carbohydrates.
        """
        return self.get_nutrient_info(food["foodNutrients"], "Carbohydrate, by difference")
