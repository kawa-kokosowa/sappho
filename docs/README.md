# Sappho Documentation

To build the documentation, you must have Sphinx, at least version 1.3,
installed. You can install it via pip:

``` shell
pip install --user sphinx
```

Then, to build the documentation, run `sphinx-build` from this directory,
like so:

``` shell
sphinx-build -b html . _build/
```

The documentation will be built into the `_build` directory.

