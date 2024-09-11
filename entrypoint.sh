#!/bin/sh

./wait-for db:3306

python flaskapp.py --host=0.0.0.0
