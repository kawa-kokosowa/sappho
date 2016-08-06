# Rules for Contributing

We want to leave your workflow up to you, and not
overload you with constraints.

## Code Philosophy

  * You are not allowed to import other modules from the Sappho package.
  * Your code should be very transparent to the fact that we're using pygame,
    that means inherit native pygame objects where possible (like surfaces
    and sprites) and return pygame or builtin Python objects. This is "loose
    coupling."
  * Other developers should not have to read about your module, as possible. To
    be truly transparent, using Sappho should be completely intuitive to a
    pygame developer.
  * Simplicity and readability first
  * Consistency
  * Fully documented (docstrings at least)

## Quality Checklist

Before making a pull request you should go through
this checklist:

  * Changes 100% tested with unit tests
  * Changes reflected in the docs
  * Docstrings thorough/complete, Google-style
  * Follows PEP8 style
  * Follows other conventions in code
  * Adheres to philosophies listed in `README.md`
  * Tests are passing, i.e., `py.test tests`
  * Run `py.test tests --doctest-modules --pep8 sappho -v --cov-report term-missing --cov=sappho`

## Git

### Branches

  * When you make a new branch, branch from master, e.g.,
    `checkout -b some-new-branch-name master`
  * Make a pull request comparing against `master`
