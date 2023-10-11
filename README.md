Pac-Man Projects - Search - Map Generator
=========================================

Simple program that generates maps/layouts for the
[Pac-Man Project - Search][pacman-project-search]
using different strategies.

 * [Requirements 📋](#Requirements-)
 * [Implemented Strategies 🎮](#Implemented-Strategies-)
 * [Authors 👨‍🎨](#Authors-)

## Requirements 📋

The project only requires Python 3.7+ and its standard library.

## Implemented Strategies 🎮

The current version implements the following list of strategies:

 * Random

    Naive implementation that generates a map setting walls
    based on the user defined *wall probability*.

 * Randomized DFS

    Uses a randomized DFS exploration to knock down walls
    between *cells*.

    It uses the user specified `width` and `height` to define
    the size of the *search* grid. But, in order to generate
    nicer looking maps, when generating the layout its final
    size will be `2 * width + 1` and `2 * height + 1`.

## Authors 👨‍🎨

 * [Josep Pon Farreny](https://github.com/jponf)

[pacman-project-search]: https://inst.eecs.berkeley.edu/~cs188/sp22/project1/