#!/usr/bin/env bash

# author Corentin GOETGHEBEUR (SNS 2023)
# Ce programme permet d'attribuer les permissions d'exécutions aux fichiers exécutables python et de les renommer.

chmod +x python_files/simji.py
mv python_files/simji.py python_files/simji

echo "Installation finished ! Go to python_files directory and try ./simji !"