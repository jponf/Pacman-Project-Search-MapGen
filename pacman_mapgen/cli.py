import argparse
import sys

from pacman_mapgen.constants import (
    DEFAULT_CYCLE_PROBABILITY,
    DEFAULT_SEED,
    DEFAULT_WALL_PROBABILTY,
)
from pacman_mapgen.core import LayoutGenerator, ProblemType
from pacman_mapgen.kruskal import KruskalLayoutGenerator
from pacman_mapgen.prim import PrimLayoutGenerator
from pacman_mapgen.randdfs import RandomizedDfsLayoutGenerator
from pacman_mapgen.randgen import RandomLayoutGenerator
from pacman_mapgen.utils.type_utils import StrEnum

################
# Main Program #
################


class LayoutMethod(StrEnum):
    """Maze generation methods."""

    PRIM = "prim"
    KRUSKAL = "kruskal"
    RANDOM = "random"
    RANDOM_DFS = "dfs"


class ProgramArgs(argparse.Namespace):
    """Typed program arguments for argparse."""

    method: LayoutMethod
    problem_type: ProblemType
    width: int
    height: int
    seed: int
    max_food: int
    cycle_probability: float
    wall_probability: float


def main():
    """Program main routine."""
    args = _parse_args()
    generator: LayoutGenerator

    try:
        generator = _create_layout_generator(args)
    except ValueError as err:
        print(f"Error: {err}.")
        sys.exit(1)

    layout = generator.generate_layout(
        problem_type=args.problem_type,
        max_food=args.max_food,
    )
    layout.print()


def _create_layout_generator(args: ProgramArgs) -> LayoutGenerator:
    if args.method is LayoutMethod.PRIM:
        return PrimLayoutGenerator(
            width=args.width,
            height=args.height,
            seed=args.seed,
            cycle_probability=args.cycle_probability,
        )
    if args.method is LayoutMethod.KRUSKAL:
        return KruskalLayoutGenerator(
            width=args.width,
            height=args.height,
            seed=args.seed,
            cycle_probability=args.cycle_probability,
        )
    if args.method is LayoutMethod.RANDOM:
        return RandomLayoutGenerator(
            width=args.width,
            height=args.height,
            seed=args.seed,
            cycle_probability=args.cycle_probability,
            wall_probability=args.wall_probability,
        )
    if args.method is LayoutMethod.RANDOM_DFS:
        return RandomizedDfsLayoutGenerator(
            width=args.width,
            height=args.height,
            seed=args.seed,
            cycle_probability=args.cycle_probability,
        )

    print(
        f"Unknown layout generator method {args.method}, expected:"
        f" {', '.join(LayoutMethod)}",
        file=sys.stderr,
    )
    sys.exit(1)


def _parse_args() -> ProgramArgs:
    parser = argparse.ArgumentParser(
        prog="gmap2.py",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--method",
        action="store",
        type=LayoutMethod,
        choices=[method.value for method in LayoutMethod],
        help="Maze generation method.",
    )

    parser.add_argument(
        "--problem-type",
        "-p",
        type=ProblemType,
        default=ProblemType.SEARCH,
        choices=[p_type.value for p_type in ProblemType],
        help="Generated problem type.",
    )

    parser.add_argument(
        "--width",
        type=int,
        required=True,
        help="Grid width. The final layout will be `2 * width + 1` wide.",
    )

    parser.add_argument(
        "--height",
        type=int,
        required=True,
        help="Grid height. The final layout will be `2 * height + 1` tall.",
    )

    parser.add_argument(
        "--seed",
        "-s",
        default=DEFAULT_SEED,
        type=int,
        help="Random number generator seed.",
    )

    parser.add_argument(
        "--max-food",
        default=10,
        type=arg_type_positive_int,
        help=f"Number of food pellets for problem-type={ProblemType.FOOD} problems",
    )

    parser.add_argument(
        "--cycle-probability",
        default=DEFAULT_CYCLE_PROBABILITY,
        type=float,
        help="Probability to connect additional nodes after the "
        "spanning-tree generation to create cycles in the layout.",
    )

    parser.add_argument(
        "--wall-probability",
        default=DEFAULT_WALL_PROBABILTY,
        type=float,
        help=f"Probability of cell becoming a wall (applies to: {LayoutMethod.RANDOM})",
    )

    return parser.parse_args(namespace=ProgramArgs())


def arg_type_positive_int(raw_value: str) -> int:
    """Function that acts as an argparse type for positive integers.

    Args:
        raw_value: Raw value provided by argparse.

    Returns:
        The value of `raw_value` as an int.

    Raises:
        ArgumentTypeError: If the value is not a positive integer.
    """
    try:
        ivalue = int(raw_value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"value '{raw_value}' is not an integer")
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(
            f"{raw_value} is an invalid positive int value",
        )
    return ivalue


###############################################################################

if __name__ == "__main__":
    main()
