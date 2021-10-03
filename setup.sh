#!/usr/bin/env bash

# author Corentin GOETGHEBEUR (SNS 2023)
# Ce programme permet d'attribuer les permissions d'exécutions aux fichiers exécutables python et de les renommer.

chmod +x python_files/asm.py
chmod +x python_files/iss.py

mv python_files/asm.py python_files/asm
mv python_files/iss.py python_files/iss

echo "Installation terminée, essayez ./asm ou ./iss !"