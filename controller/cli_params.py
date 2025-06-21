# sterowanie/controller.py

import argparse
from argparse import Namespace


class CLIParams:

    INFLOW_MIN      = 0.0
    INFLOW_MAX      = 20000.0
    INCOME_SUM_MIN  = 0.0
    INCOME_SUM_MAX  = 40000.0
    DEPENDENTS_MIN  = 0
    DEPENDENTS_MAX  = 10
    AGE_MIN         = 18
    AGE_MAX         = 100

    @classmethod
    def parse_args(cls) -> Namespace:
        parser = argparse.ArgumentParser(
            description="Fuzzy credit decision CLI (Type-1 & Type-2)")

        parser.add_argument(
            "--inflow",
            type=float,
            required=True,
            help=f"Average monthly inflow [{cls.INFLOW_MIN}, {cls.INFLOW_MAX}]"
        )
        parser.add_argument(
            "--income_sum",
            type=float,
            required=True,
            help=f"Sum of incomes [{cls.INCOME_SUM_MIN}, {cls.INCOME_SUM_MAX}]"
        )
        parser.add_argument(
            "--dependents",
            type=int,
            required=True,
            help=f"Number of dependents [{cls.DEPENDENTS_MIN}, {cls.DEPENDENTS_MAX}]"
        )
        parser.add_argument(
            "--age",
            type=int,
            required=True,
            help=f"Age of applicant [{cls.AGE_MIN}, {cls.AGE_MAX}]"
        )

        args = parser.parse_args()

        if not (cls.INFLOW_MIN <= args.inflow <= cls.INFLOW_MAX):
            parser.error(f"--inflow must be in [{cls.INFLOW_MIN}, {cls.INFLOW_MAX}]")
        if not (cls.INCOME_SUM_MIN <= args.income_sum <= cls.INCOME_SUM_MAX):
            parser.error(f"--income_sum must be in [{cls.INCOME_SUM_MIN}, {cls.INCOME_SUM_MAX}]")
        if not (cls.DEPENDENTS_MIN <= args.dependents <= cls.DEPENDENTS_MAX):
            parser.error(f"--dependents must be in [{cls.DEPENDENTS_MIN}, {cls.DEPENDENTS_MAX}]")
        if not (cls.AGE_MIN <= args.age <= cls.AGE_MAX):
            parser.error(f"--age must be in [{cls.AGE_MIN}, {cls.AGE_MAX}]")

        return args
