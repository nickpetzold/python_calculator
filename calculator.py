#!/usr/bin/env python3
"""
Calculator program which imports instructions from external file
and computes the result
"""

import argparse
import os


class InvalidInstructions(Exception):
    def __init__(self, msg="Instructions provided are not in the right format", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


CALCULATOR_ACTIONS = {
    "add": "__add__",
    "divide": "__truediv__",
    "multiply": "__mul__",
    "subtract": "__sub__",
    "apply": None,
}


def parse_instructions(instructions):
    """ Parse and validate instructions """
    if (
        type(instructions) != list
        or not all([type(ins) == str for ins in instructions])
        or instructions == []
    ):
        raise InvalidInstructions()

    parsed_instructions = []
    for instruction in instructions:
        # Allow for blank lines inbetween actions
        if instruction == '':
            continue

        components = instruction.lower().split()
        if len(components) != 2:
            raise InvalidInstructions()

        action, value = components
        if action not in CALCULATOR_ACTIONS.keys():
            raise ValueError(
                f"{action} is not a valid action"
            )

        try:
            value = int(value)

        except ValueError:
            raise ValueError(
                f"{value} is not a valid number"
            )

        parsed_instructions.append((action, value))

    if parsed_instructions[-1][0] != "apply":
        raise InvalidInstructions(
            "Final action in instructions must be apply"
        )

    return parsed_instructions


def read_file(filepath):
    """ Read file to list """
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"{filepath} is not a valid file path")

    with open(filepath, "r") as f:
        instructions = [x.strip() for x in f.readlines()]

    return instructions


def calculate(filepath):
    """ Receive path to instructions file """
    instructions = parse_instructions(read_file(filepath))

    for i in range(len(instructions)):
        cur_ins = instructions[i]
        if i == 0:
            value = cur_ins[1]

        if cur_ins[0] == "apply":
            break

        next_ins = instructions[i+1]
        value = getattr(
            value,
            CALCULATOR_ACTIONS[cur_ins[0]]
        )(next_ins[1])

    print(value)
    return value


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("filepath", help="Filepath of instructions")

    args = parser.parse_args()

    calculate(args.filepath)
