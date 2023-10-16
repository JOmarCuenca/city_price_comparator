import unittest
from models.city_cost import CityCostData, CostComparison
from utils.cost_comparator import compare_cost


class TestCostComparator(unittest.TestCase):

    def test_compare_cost(self):
        # Test case 1: Same costs
        city_cost_1 = CityCostData("NA", "USD", [1, 2, 3])
        city_cost_2 = CityCostData("NA", "USD", [1, 2, 3])
        expected_result = [
            CostComparison("Menú del día en zona cara de la ciudad", 1, 1),
            CostComparison("Menú completo en comida rápida", 2, 2),
            CostComparison("Pechuga de pollo (500 gr)", 3, 3)
        ]
        self.assertEqual(compare_cost(city_cost_1, city_cost_2), expected_result)

    def test_compare_cost_different(self):
        # Test case 2: Different costs
        city_cost_1 = CityCostData("NA", "USD", [1, 2, 3])
        city_cost_2 = CityCostData("NA", "USD", [2, 3, 4])
        expected_result = [
            CostComparison("Menú del día en zona cara de la ciudad", 1, 2),
            CostComparison("Menú completo en comida rápida", 2, 3),
            CostComparison("Pechuga de pollo (500 gr)", 3, 4)
        ]
        self.assertEqual(compare_cost(city_cost_1, city_cost_2), expected_result)

    def test_compare_cost_different_currencies(self):
        # Test case 3: Different currencies
        city_cost_1 = CityCostData("NA", "USD", [1, 2, 3])
        city_cost_2 = CityCostData("NA", "EUR", [1, 2, 3])
        with self.assertRaises(AssertionError):
            compare_cost(city_cost_1, city_cost_2)

    def test_compare_cost_different_number_of_costs(self):
        # Test case 4: Different number of costs
        city_cost_1 = CityCostData("NA", "USD", [1, 2, 3])
        city_cost_2 = CityCostData("NA", "USD", [1, 2])
        with self.assertRaises(AssertionError):
            compare_cost(city_cost_1, city_cost_2)