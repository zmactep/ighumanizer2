#!/bin/bash

ENV=`which env`
PYTHON=`which python2`
BASEDIR=`dirname $0`
CURDIR=`pwd`

cd $BASEDIR
$ENV PYTHONPATH=.. $PYTHON region_finder.py $@
cd $CURDIR
