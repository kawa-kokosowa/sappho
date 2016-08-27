# ![Sappho Logo (A Lyre)](logo/sappho-logo.png)

[![GitHub license](https://img.shields.io/github/license/lily-seabreeze/sappho.svg?style=flat-square)](https://raw.githubusercontent.com/lily-seabreeze/sappho/master/LICENSE)
[![PyPI Version](https://img.shields.io/pypi/v/sappho.svg?style=flat-square)](https://pypi.python.org/pypi/sappho/)
[![Code Climate](https://img.shields.io/codeclimate/github/lily-seabreeze/sappho.svg?style=flat-square)](https://codeclimate.com/github/lily-seabreeze/sappho)
[![Travis](https://img.shields.io/travis/lily-seabreeze/sappho.svg?style=flat-square)](https://travis-ci.org/lily-seabreeze/sappho)
[![Coverage Status](https://coveralls.io/repos/github/lily-seabreeze/sappho/badge.svg?branch=master)](https://coveralls.io/github/lily-seabreeze/sappho?branch=master)

Sappho is a 2D game engine written with Python (2 *and* 3) and pygame.

![sappho in action](https://github.com/lily-seabreeze/sappho/blob/master/game-demo.gif)

[Lily Seabreeze](http://lily.seabreeze.pro/) is this project's mom and owner. Be sure to checkout the `AUTHORS.md`!

## Design Philosophy

  1. Don't interfere with the way people build their pygame games
  2. We are not automating game logic
  3. Sappho modules _may not_ import other Sappho modules
  4. Inherit from pygame objects when possible; use conventional
     pygame models/architecture.
  5. Consistency.
  6. Simplicity trumps all else.
  7. Well documented.
  8. Code is easy-to-test. We show that with our 100% test coverage.

For more check `CONTRIBUTING.md`.

## Getting Started

Install pygame:

  * You can try `pip install hg+http://bitbucket.org/pygame/pygame`
    but it may not work...
  * **Ubuntu**, Python 2.7: `sudo apt install python-pygame`
  * **FreeBSD**, Python 2.7: `sudo pkg install py27-game`
  * **OSX**, Python 2.7: available in homebrew (note that there is
    a caveat in El Capitan [see: #63])
  * For any other operating system, or more details, see:
    http://www.pygame.org/download.shtml

Install `sappho` and run the demo:

  1. Install: `pip install -r requirements/main.txt .`
  2. `cd demo/`
  3. `python demo.py`

Be sure to checkout the contents of `demo.py` for a sample
on how Sappho is used.

We also have some good docs: http://sappho.lillian.link/

If you wanna contribute, please read `CONTRIBUTING.md`!
