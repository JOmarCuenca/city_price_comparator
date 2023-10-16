import argparse
from dataclasses import dataclass


@dataclass(frozen=True, repr=True, eq=True)
class Args:
    compared_cities: list[str]
    main_city: str

    @staticmethod
    def parseArgs():
        parser = argparse.ArgumentParser(
            prog="Compare cities liveability",
            description="Compare cities using real data of how expensive is to live there",)

        parser.add_argument(dest="compared_cities", nargs='+',
                            help="Cities to compare")
        parser.add_argument("--main-city", dest="main_city", nargs='?',
                            help="Main city to compare")

        args = parser.parse_args()

        if len(args.compared_cities) < 2:
            parser.error("At least 2 cities must be provided for comparison")

        return Args(
            compared_cities=args.compared_cities,
            main_city=args.main_city if args.main_city is not None else args.compared_cities[0],
        )
