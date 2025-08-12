from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from analytics.macronutrients.urls import MACRONUTRIENT_SUMMARY_NAME
from goals.models import DailyMacronutrientGoal
from intake.models import FoodEntry


def _create_food(user, d, cals, protein, carbs, fats, name="food"):
    return FoodEntry.objects.create(
        user=user,
        date=d,
        food_name=name,
        total_calories=cals,
        total_protein=protein,
        total_carbs=carbs,
        total_fats=fats,
        food_weight=100.0,
    )


def _create_goal(user, d, cals, protein, carbs, fats):
    return DailyMacronutrientGoal.objects.create(
        user=user,
        date=d,
        goal_calories=cals,
        goal_protein=protein,
        goal_carbs=carbs,
        goal_fats=fats,
    )


class MacronutrientAnalyticsViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(id=1, username="Test User")

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.other_user = User.objects.create_user(
            username="other_user", email="other_user@example.com", password="pass1234"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.start = date(2025, 8, 1)
        self.end = date(2025, 8, 7)
        self.url = reverse(MACRONUTRIENT_SUMMARY_NAME)

    def _d(self, days: int) -> date:
        return self.start + timedelta(days=days)

    def test_validation_start_after_end(self):
        resp = self.client.get(self.url, {"start": "2025-08-10", "end": "2025-08-01"})
        self.assertEqual(resp.status_code, 400)
        self.assertIn("start", str(resp.data).lower())

    def test_empty_range_returns_zero_summary(self):
        _create_goal(self.user, self._d(0), 2000, 50, 275, 70)

        resp = self.client.get(
            self.url,
            {"start": self.start.isoformat(), "end": self.end.isoformat()},
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["daysWithLogs"], 0)

        summary = resp.data["summary"]
        for nutrient in ["calories", "protein", "carbs", "fats"]:
            self.assertAlmostEqual(summary[nutrient]["totalConsumed"], 0.0)
            self.assertAlmostEqual(summary[nutrient]["totalGoal"], 0.0)
            self.assertAlmostEqual(summary[nutrient]["percentageOfGoal"], 0.0)
            self.assertAlmostEqual(summary[nutrient]["averageConsumed"], 0.0)

    def test_days_with_logs_counts_distinct_entry_days(self):
        _create_food(self.user, self._d(0), 300, 15, 30, 10)
        _create_food(self.user, self._d(0), 200, 10, 20, 5)
        _create_food(self.user, self._d(2), 500, 25, 50, 15)

        resp = self.client.get(self.url, {"start": self.start.isoformat(), "end": self.end.isoformat()})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["daysWithLogs"], 2)

        self.assertAlmostEqual(resp.data["summary"]["calories"]["totalConsumed"], 1000.0)

        self.assertAlmostEqual(resp.data["summary"]["calories"]["averageConsumed"], 1000.0 / 2.0)

    def test_aggregation_and_percentages(self):
        day0_food1_cals, day0_food1_protein, day0_food1_carbs, day0_food1_fats = 600, 30, 80, 20
        day0_food2_cals, day0_food2_protein, day0_food2_carbs, day0_food2_fats = 400, 20, 40, 10
        day2_food_cals, day2_food_protein, day2_food_carbs, day2_food_fats = 1000, 60, 120, 40

        _create_food(self.user, self._d(0), day0_food1_cals, day0_food1_protein, day0_food1_carbs, day0_food1_fats)
        _create_food(self.user, self._d(0), day0_food2_cals, day0_food2_protein, day0_food2_carbs, day0_food2_fats)
        _create_food(self.user, self._d(2), day2_food_cals, day2_food_protein, day2_food_carbs, day2_food_fats)

        goal_day0_cals, goal_day0_protein, goal_day0_carbs, goal_day0_fats = 2000, 50, 275, 70
        goal_day2_cals, goal_day2_protein, goal_day2_carbs, goal_day2_fats = 1900, 55, 260, 65
        goal_day4_cals, goal_day4_protein, goal_day4_carbs, goal_day4_fats = 2100, 60, 300, 80

        _create_goal(self.user, self._d(0), goal_day0_cals, goal_day0_protein, goal_day0_carbs, goal_day0_fats)
        _create_goal(self.user, self._d(2), goal_day2_cals, goal_day2_protein, goal_day2_carbs, goal_day2_fats)
        _create_goal(self.user, self._d(4), goal_day4_cals, goal_day4_protein, goal_day4_carbs, goal_day4_fats)

        _create_goal(self.user, self._d(8), 999, 9, 9, 9)
        _create_food(self.other_user, self._d(0), 9999, 999, 999, 999)
        _create_goal(self.other_user, self._d(0), 9999, 999, 999, 999)

        total_cals_consumed = day0_food1_cals + day0_food2_cals + day2_food_cals
        total_protein_consumed = day0_food1_protein + day0_food2_protein + day2_food_protein
        total_carbs_consumed = day0_food1_carbs + day0_food2_carbs + day2_food_carbs
        total_fats_consumed = day0_food1_fats + day0_food2_fats + day2_food_fats

        # Do not include goal_day_4 in these calculations because they have no entries on the associated date.
        total_cals_goal = goal_day0_cals + goal_day2_cals
        total_protein_goal = goal_day0_protein + goal_day2_protein
        total_carbs_goal = goal_day0_carbs + goal_day2_carbs
        total_fats_goal = goal_day0_fats + goal_day2_fats

        resp = self.client.get(self.url, {"start": self.start.isoformat(), "end": self.end.isoformat()})
        self.assertEqual(resp.status_code, 200)

        data = resp.data
        self.assertEqual(data["startDate"], self.start.isoformat())
        self.assertEqual(data["endDate"], self.end.isoformat())
        self.assertEqual(data["daysWithLogs"], 2)

        # --- Assertions: Consumed ---
        self.assertAlmostEqual(data["summary"]["calories"]["totalConsumed"], total_cals_consumed)
        self.assertAlmostEqual(data["summary"]["protein"]["totalConsumed"], total_protein_consumed)
        self.assertAlmostEqual(data["summary"]["carbs"]["totalConsumed"], total_carbs_consumed)
        self.assertAlmostEqual(data["summary"]["fats"]["totalConsumed"], total_fats_consumed)

        # --- Assertions: Goals ---
        self.assertAlmostEqual(data["summary"]["calories"]["totalGoal"], total_cals_goal)
        self.assertAlmostEqual(data["summary"]["protein"]["totalGoal"], total_protein_goal)
        self.assertAlmostEqual(data["summary"]["carbs"]["totalGoal"], total_carbs_goal)
        self.assertAlmostEqual(data["summary"]["fats"]["totalGoal"], total_fats_goal)

        # --- Assertions: Percent ---
        self.assertAlmostEqual(
            data["summary"]["calories"]["percentageOfGoal"], (total_cals_consumed / total_cals_goal) * 100.0
        )

        # --- Assertions: Average ---
        self.assertAlmostEqual(data["summary"]["calories"]["averageConsumed"], total_cals_consumed / 2.0, places=6)

    def test_entries_no_goals_defaults_to_zero(self):
        d = self._d(0)

        food_cals, food_protein, food_carbs, food_fats = 500.0, 30.0, 40.0, 10.0
        expected_goal_default = 0.0
        expected_percentage_default = 0.0

        _create_food(self.user, d, food_cals, food_protein, food_carbs, food_fats)

        resp = self.client.get(self.url, {"start": d.isoformat(), "end": d.isoformat()})
        self.assertEqual(resp.status_code, 200)

        s = resp.data["summary"]

        # Consumed
        self.assertAlmostEqual(s["calories"]["totalConsumed"], food_cals)
        self.assertAlmostEqual(s["protein"]["totalConsumed"], food_protein)
        self.assertAlmostEqual(s["carbs"]["totalConsumed"], food_carbs)
        self.assertAlmostEqual(s["fats"]["totalConsumed"], food_fats)

        # Goals
        self.assertAlmostEqual(s["calories"]["totalGoal"], expected_goal_default)
        self.assertAlmostEqual(s["protein"]["totalGoal"], expected_goal_default)
        self.assertAlmostEqual(s["carbs"]["totalGoal"], expected_goal_default)
        self.assertAlmostEqual(s["fats"]["totalGoal"], expected_goal_default)

        # Percentages
        self.assertAlmostEqual(s["calories"]["percentageOfGoal"], expected_percentage_default)
        self.assertAlmostEqual(s["protein"]["percentageOfGoal"], expected_percentage_default)
        self.assertAlmostEqual(s["carbs"]["percentageOfGoal"], expected_percentage_default)
        self.assertAlmostEqual(s["fats"]["percentageOfGoal"], expected_percentage_default)

        # Average
        self.assertAlmostEqual(s["calories"]["averageConsumed"], food_cals)
