# Miscellaneous files

* `sappho.sublime-project` is a Sublime Text project file for Sappho that
  includes build tasks for running tests and building the documentation.
* `annotatetilesheet.py` is a script that annotates tilesheets with the
  ID of each tile, optionally drawing a border around the tiles.

  It produces output that looks like this:

  ![](annotatetilesheet-example.png)
* `pre-commit`: This script runs all the tests before you commit and prevents
  you from committing if you fail. Copy `pre-commit` to `.git/hooks/pre-commit`.
