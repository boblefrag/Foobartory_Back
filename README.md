# Foobartory

Foobartory is an application that let you create foobars and eventualy
create a factory of 30 workers. Creating foobar follows some rules but
in a world of changes we do know those rules can change. Foobartory
implement a rule manager that you can change when rules change.

In the same way, new workers with new capabilities, faster or more
effctive can be invented. Foobartory take this into account and give
you easy ways to change the way workers works.

Of course you need bars and foos to create foobars that you will
convert into new workers because what you really want is 30 workers
but the real currency that make your factory efficient is time.

In this game we take time as a currency. It give you the ability to
run the program wth different strategies and find quickly the sweet
spot to win the game the fastest way possible.

## Install

This project use `python` as programing language. it needs version >=3.7
For dependancies management we use poetry
https://python-poetry.org/docs/

dependencies are only needed if you want to develop or run the
test. To run the main program `python3` will be enough

Dependancies are listed in `pyproject.toml`

## Run

To run the program `cd` to `foobar_workers` in the same directory as
this `README` and type

```shell
python run.py
```

## Play

To change some parts of the rules you can get a look at
`foobar_workers/workers.py`

You will find `REQUIREMENTS` and `RETRIBUTIONS`

Here you will be able to change what we need to create reessources and
what we gain creating some (respectively)


In order to change the way the manager work, you can edit the `run`
function and find the sweet spot between ressource creation order and
ressources count.

You can also play with the `__init__` method if you want to create
more or less than 2 workers for the first run.

## Testing

As stated above, you will need pytest tu run the tests. simply issue:

```shell
pytest
```
 in the current directory.

 Tests are located in the tests/ directory.


## Architecture

Architecture is very basic.

- Workers
- Manager

### Workers

Workers manage their ressources (seconds) and create what the manager
told them to. They need to pay ressources they consume (even if some
are on the manager) and get created ressources back to the manager

### Manager

There is only one manager per game
It keep track of the worker status, his own ressources (foos, bars,
foobars, etc...) and give order to the workers for the ressources
creations


## What could be improved

### functonal

  there's a lot of foos and bars at the end of the runs, this is a
  hint that the strategy is not optimal.

### code
- typehint could add better understanding on what we are working on
- less `getattr` and `settatr`. it make the code difficult to read
- black as a formating tool would be nice
- isort to sort imports (there's not a lot of them)

### testing
- a bit of coverage would be nice. I don't think everything is well
  tested
