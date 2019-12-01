#!/bin/sh

#Argumento do nome do arquivo
#notebook=$1

notebook="PI 4.ipynb"

jupyter nbconvert --to python 'PI 4.ipynb'

echo '$notebook Convertido!'
