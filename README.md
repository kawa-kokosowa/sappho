# ![Sappho Logo (A Lyre)](logo/sappho-logo.png)

[![GitHub license](https://img.shields.io/github/license/lillian-gardenia-seabreeze/sappho.svg?style=flat-square)](https://raw.githubusercontent.com/lillian-gardenia-seabreeze/sappho/master/LICENSE)
[![PyPI Version](https://img.shields.io/pypi/v/sappho.svg?style=flat-square)](https://pypi.python.org/pypi/sappho/)
[![Code Climate](https://img.shields.io/codeclimate/github/lillian-gardenia-seabreeze/sappho.svg?style=flat-square)](https://codeclimate.com/github/lillian-gardenia-seabreeze/sappho)
[![Travis](https://img.shields.io/travis/lillian-gardenia-seabreezee/sappho.svg?style=flat-square)](https://travis-ci.org/lillian-gardenia-seabreeze/sappho)
[![Coverage Status](https://coveralls.io/repos/github/lillian-gardenia-seabreeze/sappho/badge.svg?branch=master)](https://coveralls.io/github/lillian-gardenia-seabreeze/sappho?branch=master)
[![Donate with Paypal](https://img.shields.io/badge/paypal-donate-ff69b4.svg?style=flat-square)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=ZU5EVKVY2DX2S)

Sappho is a 2D game engine written with Python and pygame.

![sappho in action](https://github.com/lillian-gardenia-seabreeze/sappho/blob/master/game-demo.gif)

[Lillian Gardenia Seabreeze](http://about.lillian.link/) is this project's mom and owner. Be sure to checkout the `AUTHORS.md`!

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

## Getting Started

  1. Install: `pip install -r requirements/main.txt .`
  2. `cd demo/`
  3. `python demo.py`

Be sure to checkout the contents of `demo.py` for a sample
on how Sappho is used.

We also have some good docs: http://sappho.lillian.link/

If you wanna contribute, please read `CONTRIBUTING.md`!
