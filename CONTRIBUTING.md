# Rules for Contributing

## Before you start (code philosophy)

  * You are not allowed to import other modules from the Sappho package.
  * Your code should be very transparent to the fact that we're using pygame,
    that means inherit native pygame objects where possible (like surfaces
    and sprites) and return pygame or builtin Python objects. This is "loose
    coupling." Don't interfere with the way people build their pygame games.
  * Other developers should not have to read about your module, as possible. To
    be truly transparent, using Sappho should be completely intuitive to a
    pygame developer.
  * Simplicity and readability first
  * Consistency
  * Fully documented (docstrings at least)
  * Create code that is easy to test. 100% test coverage.
  * Don't automate "game logic"
  * Avoid modifying foreign objects inside of a different object
  * Use `etc/pre-commit` git hook

I like to think of an object as a data structure, so I make my `__init__()`
method accept only its data structure, it itself does not construct the data/
data structure. There are class methods for constructing said data structure/data,
and methods for manipulating it, navigating it. Think of a tile map; it's inherently
a 2D grid of tiles, so the data structure is a 2d list of tile objects. Your
`__init__()` method should be exclusively assignment statements, with at most
basic calculations being performed.

## Acceptance criteria for pull requests

First you'll want to make a branch that identifies the set of changes
you intend to make, consider:

  * `feature/collide-line-heuristics`
  * `fix/32-animate-bug`
  * `clean/refactor-and-add-comments`
  * `test/tiles-raise-some-exception`

Use `git checkout -b docs/sphinx-and-docstrings master`.

After your branch is created, make sure each commit has a descriptive
`git commit` message. You're invited to make a pull request for your
branch whenever you please, but keep in mind the acceptance criteria
for pull requests:

  * Changes 100% tested with unit tests
  * Changes reflected in the docs
  * Docstrings thorough/complete, Google-style
  * Follows PEP8 style
  * Follows other conventions in code
  * Adheres to philosophies listed in `README.md`
  * Tests are passing, i.e., `py.test tests`
  * Tests passing in Travis CI (tip: use `etc/pre-commit`)

Once your pull request has been reviewed by one other developer
(signified by their approval, e.g., :+1:) it may be merged to `nextrelease`,
but that's ultimately up to Lily Seabreeze, the project's mom who
manages the project and its releases.

## Running tests

`pip install -r requirements/develop.txt`

`py.test tests --doctest-modules --pep8 sappho -v --cov-report term-missing --cov=sappho`
