# DEVSIM

This is a prototype for an Object Oriented framework for simulating semiconductor devices using devsim.

This was developed as a project on the Google Summer of Code 2018. Go to [GSOC_2018_Report.md](GSOC_2018_Report.md) for the details.


# How to run this?

You need to install devsim. Once you've installed it create a virtualenv with your favorite tool. Replace the python binary of your virtualenv with the devsim interpreter.You must see something like this when typing `python` (inside your virtualenv):

```bash
$> python
----------------------------------------

 DEVSIM

 Version: Beta 0.01

 Copyright 2009-2018 Devsim LLC

----------------------------------------


Python 3.6.6 (default, Jul 19 2018, 14:25:17) 
[GCC 8.1.1 20180712 (Red Hat 8.1.1-5)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```

Now you need to install this package in developer mode:

```bash
python setup.py develop
```
This will link the devsim directory into the PYTHON_PATH. You can run the examples like this:

```bash
python devsim/examples/solar_cell.py
```

Only Python 3 is supported.
I wrote this code in a Fedora machine, you will need to change the commands according to you OS.

## Run tests

``` bash
devsim setup.py test
```
