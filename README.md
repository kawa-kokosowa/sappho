# ![Sappho Logo (A Lyre)](logo/sappho-logo.png)

[![GitHub license](https://img.shields.io/github/license/lillian-lemmer/sappho.svg?style=flat-square)](https://raw.githubusercontent.com/lillian-lemmer/sappho/master/LICENSE)
[![PyPI Version](https://img.shields.io/pypi/v/sappho.svg?style=flat-square)](https://pypi.python.org/pypi/sappho/)
[![Code Climate](https://img.shields.io/codeclimate/github/lillian-lemmer/sappho.svg?style=flat-square)](https://codeclimate.com/github/lillian-lemmer/sappho)
[![Donate with Paypal](https://img.shields.io/badge/paypal-donate-ff69b4.svg?style=flat-square)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=ZU5EVKVY2DX2S)

Sappho is a 2D game engine written with Python and pygame.

The purpose of this repo is to rewrite Hypatia Engine
and eventually replace Hypatia Engine as "Sappho."

[Lillian Gardenia Seabreeze](http://about.lillian.link/) is this project's mom and owner.

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

  1. Install: `pip install -r requirements.txt .`
  2. `cd demo/`
  3. `python demo.py`

Be sure to checkout the contents of `demo.py` for a sample
on how Sappho is used.

We also have some good docs: http://sappho.hypatiasoftware.org/

If you wanna contribute, please read `CONTRIBUTING.md`!
