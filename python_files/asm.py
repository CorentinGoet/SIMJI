#!/usr/bin/env python3

"""
@author Corentin GOETGHEBEUR (SNS 2023)
Fichier python exécutable de traduction du code assembleur en binaire.
"""

import sys
from assembleur import Assembleur

if __name__ == "__main__":
    # gestion des arguments d'entrée
    if len(sys.argv) == 1:  # texte d'accueil
        print("Ce programme est un traducteur de code assembleur vers du code machine binaire.\n" +
              "Pour avoir des informations de syntaxe, essayez ./asm -h.")

    elif len(sys.argv) == 2:  # un seul argument

        if sys.argv[1] in ["-h", "--help"]:  # module d'aide
            print("./asm monFichier.asm \n" +
                  "\t Traduit le fichier assembleur en code binaire et le stocke dans le dossier instruction_files" +
                  "sous le nom 'instructions.hex'. \n" +
                  "./asm -h   ou  ./asm --help \n" +
                  "\t affiche l'aide de syntaxe.\n"
                  "./asm monFichier.asm monDossier/monFichier.hex \n" +
                  "\t Traduit le fichier assembleur et le stocke dans le dossier monDossier sous le nom monFichier.hex.\n")
        else:
            # Traduction en binaire du fichier assembleur
            try:
                fileName = sys.argv[1]
                asm = Assembleur(fileName)
                for i in range(len(asm.instrList)):
                    instr = asm.getInstrNum(i)
                    asm.writeInstr(instr, i)

            except FileNotFoundError:
                print("Fichier introuvable.")

            except Exception:
                print("Erreur d'exécution.")

    elif len(sys.argv) == 3:
        inputFile = sys.argv[1]
        outputFile = sys.argv[2]
        try:
            # effacer le contenu du fichier output si il existe
            f = open(outputFile, 'w')
            f.write('')
            f.close()
            # Traduction et écriture
            asm = Assembleur(inputFile)
            for i in range(len(asm.instrList)):
                instr = asm.getInstrNum(i)
                asm.writeInstr2(instr, i, outputFile)

        except FileNotFoundError:
            print("Fichier introuvable.")

        except Exception:
            print("Erreur d'exécution.")
