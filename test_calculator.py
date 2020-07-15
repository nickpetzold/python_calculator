import unittest
import os

import mock

from calculator import calculate, InvalidInstructions

_ = "dummy_filepath"
TEST_FILEPATH = os.path.join(os.path.dirname(__file__), "test_instructions.txt")


class TestCalculator(unittest.TestCase):
    @mock.patch('calculator.read_file')
    def test_calculator_success(self, rf):
        rf.return_value = [
            "add 2",
            "multiply 3",
            "apply 3",
        ]

        self.assertEqual(calculate(_), 15)

        rf.return_value = [
            "divide 4",
            "multiply 2",
            "apply 3",
        ]

        self.assertEqual(calculate(_), 6)

        rf.return_value = [
            "divide -4",
            "multiply 2",
            "subtract 10",
            "apply 3",
        ]

        self.assertEqual(calculate(_), -23)

        rf.return_value = [
            "divide 44",
            "multiply -4",
            "subtract -10",
            "add 100",
            "multiply 6",
            "apply 3",
        ]

        self.assertEqual(calculate(_), 48)

        rf.return_value = [
            "add 100",
            "add 200",
            "add 300",
            "add 400",
            "add 500",
            "apply 3",
        ]

        self.assertEqual(calculate(_), 1503)

    @mock.patch('calculator.read_file')
    def test_calculator_success_apply_only(self, rf):
        rf.return_value = [
            "apply 3",
        ]

        self.assertEqual(calculate(_), 3)

    def test_calculator_success_with_input_file(self):
        self.assertEqual(calculate(TEST_FILEPATH), 774497)

    @mock.patch('calculator.read_file')
    def test_calculator_invalid_instructions(self, rf):
        rf.return_value = [
            "add 100",
            "add 200",
            "apply 3",
            "add 300",
            "add 400",
            "add 500",
        ]

        with self.assertRaises(InvalidInstructions):
            calculate(_)

    @mock.patch('calculator.read_file')
    def test_calculator_empty_instructions(self, rf):
        rf.return_value = []

        with self.assertRaises(InvalidInstructions):
            calculate(_)

    @mock.patch('calculator.read_file')
    def test_calculator_invalid_action(self, rf):
        rf.return_value = [
            "add 100",
            "add 200",
            "add 300",
            "foo 400",
            "add 500",
            "apply 3",
        ]

        with self.assertRaises(ValueError):
            calculate(_)

    @mock.patch('calculator.read_file')
    def test_calculator_invalid_value(self, rf):
        rf.return_value = [
            "add 100",
            "add 200",
            "add 300",
            "foo 400",
            "add bar",
            "apply 3",
        ]

        with self.assertRaises(ValueError):
            calculate(_)

    @mock.patch('calculator.read_file')
    def test_calculator_whitespace_success(self, rf):
        rf.return_value = [
            "add 2       ",
            "multiply       3",
            "divide 6",
            "         apply 3",
        ]

        self.assertEqual(calculate(_), 10)

    def test_calculator_invalid_filepath(self, ):
        with self.assertRaises(FileNotFoundError):
            calculate("/some/invalid/path")
