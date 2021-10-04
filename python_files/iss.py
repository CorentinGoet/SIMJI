#!/usr/bin/env python3

"""
@author Corentin GOETGHEBEUR (SNS 2023)
Ce fichier exécute le jeu d'instruction correspondant au fichier binaire fourni en argument.
"""
#a
import sys
from VM import VM
from Memory import Memory, Cache

if __name__ == '__main__':

    # gestion des arguments d'entrée

    if len(sys.argv) == 1:
        print("Ce programme est un simulateur de jeu d'instruction. Pour afficher l'aide de syntaxe, ./iss -h.")

    elif len(sys.argv) == 2:

        # Aide de syntaxe
        if sys.argv[1] in ["-h", "--help"]:
            print("./iss monFichier.hex \n" +
                  "\t exécute les instructions du programme monFichier.hex à partir d'une mémoire vide.\n" +
                  "./iss monFichier.hex memoire.hex\n" +
                  "\t Execute les instructions du programme monFichier.hex à partir de la mémoire fournie dans le fichier memoire.hex." +
                  "\n \n La mémoire finale est stockée sous output_files/memoire.hex. \n" +
                  "Options :\n"
                  "\t -c : affiche le cache. \n" +
                  "\t -m : affiche le début de la mémoire. \n" +
                  "\t -ma : affiche toute la mémoire.")

        # execution
        else:
            try:
                inputFile = sys.argv[1]
                print("Création de la mémoire ...")
                dataMem = Memory()
                print("Création du cache ...")
                cache = Cache(dataMem)
                print("Exécution des instructions du fichier {} ...".format(inputFile))
                vm = VM(inputFile, cache)
                vm.run()
                print("Ecriture du fichier de mémoire ...")
                vm.cache.memory.writeMem("../output_files/memoire.hex")

                print("Exécution terminée")

            except FileNotFoundError:
                print("Fichier introuvable.")
            except Exception as e:
                print("Erreur d'execution.")
                print(e)

    elif len(sys.argv) == 3:
        # si le 2e argument est une option
        if sys.argv[2][0] == '-':
            try:
                inputFile = sys.argv[1]
                print("Création de la mémoire ...")
                dataMem = Memory()
                print("Création du cache ...")
                cache = Cache(dataMem)
                print("Exécution des instructions du fichier {} ...".format(inputFile))
                vm = VM(inputFile, cache)
                vm.run()
                print("Ecriture du fichier de mémoire ...")
                vm.cache.memory.writeMem("../output_files/memoire.hex")

                if 'c' in sys.argv[2]:
                    print(vm.cache)
                if 'ma' in sys.argv[2]:
                    print(vm.cache.memory)
                elif 'm' in sys.argv[2]:
                    vm.cache.memory.displayMem()

                print("Exécution terminée")

            except FileNotFoundError:
                print("Fichier introuvable.")
            except Exception:
                print("Erreur d'execution.")

        # fichier d'instructions et memoire
        else:
            try:
                inputFile = sys.argv[1]
                memFile = sys.argv[2]
                print("Chargement de la mémoire ...")
                dataMem = Memory()
                dataMem.loadMem(memFile)
                print("Création du cache ...")
                cache = Cache(dataMem)
                print("Exécution des instructions du fichier {} ...".format(inputFile))
                vm = VM(inputFile, cache)
                vm.run()
                print("Ecriture du fichier de mémoire ...")
                vm.cache.memory.writeMem("../output_files/memoire.hex")

                print("Exécution terminée")

            except FileNotFoundError:
                print("Fichier introuvable.")
            except Exception as e:
                print("Erreur d'execution.")
                print(e)

    elif len(sys.argv) == 4:
        try:
            inputFile = sys.argv[1]
            memFile = sys.argv[2]
            print("Chargement de la mémoire ...")
            dataMem = Memory()
            dataMem.loadMem(memFile)
            print("Création du cache ...")
            cache = Cache(dataMem)
            print("Exécution des instructions du fichier {} ...".format(inputFile))
            vm = VM(inputFile, cache)
            vm.run()
            print("Ecriture du fichier de mémoire ...")
            vm.cache.memory.writeMem("../output_files/memoire.hex")

            if 'c' in sys.argv[3]:
                print(vm.cache)
            if 'ma' in sys.argv[3]:
                print(vm.cache.memory)
            elif 'm' in sys.argv[3]:
                vm.cache.memory.displayMem()

            print("Exécution terminée")

        except FileNotFoundError:
            print("Fichier introuvable.")
        except Exception as e:
            print("Erreur d'execution.")
            print(e)
