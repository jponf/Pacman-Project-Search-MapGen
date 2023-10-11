Pac-Man Projects - Search - Map Generator
=========================================

Simple program that generates maps/layouts for the
[Pac-Man Project - Search][pacman-project-search]
using different strategies.

 * [Requirements 📋](#Requirements-)
 * [Implemented Strategies 🎮](#Implemented-Strategies-)
 * [Command Line Interface 💻](#Command-Line-Interface-)
 * [Authors 👨‍🎨](#Authors-)

## Requirements 📋

The project only requires Python 3.7+ and its standard library.

Additionally, since some generated maps may not place the `goal`
on the *bottom*-*left* corner. Make sure to change *searchAgents.py*
line 190 to set the `goal` to wherever the *food* is on the map:

```python
self.goal = gameState.getFood().asList()[0]
```

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

## Command Line Interface 💻

To run the program on a terminal use the following command:

```console
python3 -m pacman_mapgen --height <height> --width <width> --method <method> --seed <seed>...
```

The options shown above are the ones that are common to all *methods*. Use
`--help` to get a more details about the supported parameters.

### Example

```
python3 -m pacman_mapgen --method dfs --width 10 --height 10 --seed 1234
```

Generates the output:

```
%%%%%%%%%%%%%%%%%%%%%
% %     %           %
% % % %%% %%%%%%% %%%
%   %   %   %   %   %
% %%%%% %%% %%% %%% %
% %   %        .% % %
% % % %%%%%%%%%%% % %
%   % % %         % %
%%%%% % % %%%%%%%%% %
%     % %       %   %
% %%%%% %%%%%%% % % %
%           %   % % %
%%%%%%%%%%%%% %%% %%%
%         %  P%     %
% %%%%%%% % %%% %%% %
% %     %   % %   % %
% %%% %%%%%%% % %%% %
%   %       %   %   %
%%% %%%%% % %%%%% % %
%         %       % %
%%%%%%%%%%%%%%%%%%%%%
```
To save the generated map/layout simply redirect the output to a file:

```
python3 -m pacman_mapgen --method dfs --width 10 --height 10 --seed 1234 > randdfsMaze.lay
```


## Authors 👨‍🎨

 * [Josep Pon Farreny](https://github.com/jponf)

[pacman-project-search]: https://inst.eecs.berkeley.edu/~cs188/sp22/project1/