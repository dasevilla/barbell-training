A simple script to generate a training program described in the book
[Starting Strength](http://startingstrength.com/). See the
[sample routine](https://github.com/dasevilla/barbell-training/raw/master/sample.pdf).


# Requirements

The `Jinja2` Python module and the `pdflatex` command.


# Usage

You need to update the exercises defined in the `main` method of `strength.py`
to match you current level. Once updated, a simple `make default` will build a
PDF.
