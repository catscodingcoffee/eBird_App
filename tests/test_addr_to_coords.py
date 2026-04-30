import unittest
from main import get_coordinates  # import whatever you want to test

class TestEbirdApp(unittest.TestCase):

    def test_get_coordinates_valid_address(self):
        lat, lng = get_coordinates("13134, SW Tamera Ln Tigard, OR")
        self.assertAlmostEqual(lat, 45.43, places=1)
        self.assertAlmostEqual(lng, -122.81, places=1)

    def test_get_coordinates_invalid_address(self):
        self.assertEqual(get_coordinates("asdfjkl;qwerty"),"Address not found")

if __name__ == "__main__":
    unittest.main()