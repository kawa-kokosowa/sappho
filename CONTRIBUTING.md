# Rules for Contributing

We want to leave your workflow up to you, and not
overload you with constraints.

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

## Git

### Branches

  * When you make a new branch, branch from master, e.g.,
    `checkout -b some-new-branch-name master`
  * Make a pull request comparing against `master`

### Releases

  * Each pull request reviewed by Lillian Lemmer
  * `master` is for releases
  * Delete merged branches
  * Tag release after merging a branch and setting
    the version in `__init__.py`. Once commit is made,
    run `./distrib.sh`. Make sure to edit/sign tag
    on GitHub!
