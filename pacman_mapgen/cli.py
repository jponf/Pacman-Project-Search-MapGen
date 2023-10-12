import argparse
from enum import Enum

from pacman_mapgen.core import LayoutGenerator
from pacman_mapgen.randdfs import RandomizedDfsLayoutGenerator
from pacman_mapgen.randgen import RandomLayoutGenerator


################
# Main Program #
################


class MazeMethod(str, Enum):
    RANDOM = "random"
    RANDOM_DFS = "dfs"


class ProgramArgs(argparse.Namespace):
    method: MazeMethod
    width: int
    height: int
    seed: int
    wall_probability: float


def main():
    args = _parse_args()
    generator: LayoutGenerator

    if args.method is MazeMethod.RANDOM:
        generator = RandomLayoutGenerator(
            width=args.width,
            height=args.height,
            seed=args.seed,
            wall_probability=args.wall_probability,
        )
    elif args.method is MazeMethod.RANDOM_DFS:
        generator = RandomizedDfsLayoutGenerator(
            width=args.width,
            height=args.height,
            seed=args.seed,
        )

    layout = generator.generate_layout()
    layout.print()


def _parse_args() -> ProgramArgs:
    parser = argparse.ArgumentParser(
        prog="gmap2.py",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--method",
        action="store",
        type=MazeMethod,
        choices=[method.value for method in MazeMethod],
        help="Maze generation method.",
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
        default=1234,
        type=int,
        help="Random number generator seed.",
    )

    parser.add_argument(
        "--wall-probability",
        default=0.3,
        type=float,
        help=f"Probability of cell becoming a wall (applies to: {MazeMethod.RANDOM})",
    )

    return parser.parse_args(namespace=ProgramArgs)


###############################################################################

if __name__ == "__main__":
    main()
