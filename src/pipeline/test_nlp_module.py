from path_generator import LearningPathGenerator as l
import unittest


class TestNLPModule(unittest.TestCase):
    def test_valid_query(self):
        valid_query = "I want to learn python"
        valid_output = "python"
        self.assertEqual(l(valid_query, "beginner").extract_keyword(), valid_output)

    def test_invalid_query(self):
        invalid_query = "I want to learn hindi"
        with self.assertRaises(ValueError) as ctx:
            l(invalid_query, "beginner")
        self.assertEqual(str(ctx.exception), "invalid query")


if __name__ == "__main__":
    unittest.main()
