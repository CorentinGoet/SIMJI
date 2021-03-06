"""
@author Corentin GOETGHEBEUR (SNS 2023)
Fichier contenant les classes de modélisation de la mémoire.
"""


class Storage:

    def __init__(self, size=1024):
        self.size = size
        self.mem = [0] * self.size

    def write(self, address, data):
        """
        Méthode d'écriture sur la mémoire.
        :param address: adresse où écrire.
        :param data: donnée à écrire.
        :return: None
        """
        if data < 0:
            data = (1 << 32) + data
        self.mem[address] = data

    def read(self, address):
        """
        Méthode de lecture de la mémoire.
        :param address: adresse où lire.
        :return: donnée correspondant à l'adresse.
        """
        return self.mem[address]

    def burst_read(self, address, burst_size):
        """
        Méthode de lecture en rafale de la mémoire.
        :param address: adresse minimale
        :param burst_size: taille de la rafale.
        :return: Ensemble des données récupérées lors de la rafale.
        """
        res = []
        for i in range(burst_size):
            res.append(self.read(address + i))     # on ajoute au résultat la donnée correspondant aux adresses
        return res

    def loadMem(self, fileName):
        """
        Chargement de la mémoire à partir d'un fichier.
        :param fileName: nom du fichier contenant la mémoire.
        :return: None
        """

        f = open(fileName, 'r')
        memList = f.readlines()
        f.close()
        for i in range(len(memList)):
            data = memList[i].split(" ")[1]
            self.write(i, int(data, 16))

    def writeMem(self, outputFile):
        """
        Ecrit le contenu de la mémoire dans le fichier outputFile.
        :param outputFile: nom du fichier de sortie
        :return: None
        """
        f = open(outputFile, 'w')
        for i in range(len(self.mem)):
            f.write(str(hex(i)) + " " + str(hex(self.mem[i])) + " \n")
        f.close()

    def __str__(self):
        s = "#"*50 + "\n"
        s += "---------   Storage   --------- \n"
        s += "Address".ljust(9, ' ') + "Value \n"
        for i in range(self.size):
            s += str(hex(i)).ljust(9, ' ')
            s += str(hex(self.mem[i]))
            s += "\n"
        return s

    def displayMem(self, n=10):
        """
        Affichage partiel de la mémoire.
        :param n: nombre de lignes à afficher
        :return: None
        """
        s = "#" * 50 + "\n"
        s += "---------   Storage   --------- \n"
        s += "Address".ljust(9, ' ') + "Value \n"
        for i in range(min(self.size, n)):
            s += str(hex(i)).ljust(9, ' ')
            s += str(hex(self.mem[i]))
            s += "\n"

        if self.size > n:
            s += "...\n"

        print(s)


class Cache:
    """
    Classe modélisant un cache à correspondance directe.
    On considére un cache à 16 lignes donc 4 bits pour le numéro de lignes.
    Les lignes contiennent 8 blocs donc 3 bits de l'adresse servent à l'offset.
    Il reste donc 3 bits pour le tag.
    """

    def __init__(self, memory, size=16):
        """
        Constructeur de la classe cache.
        :param memory: Mémoire source
        :param size: Nombre de lignes (Ne changer la valeur par défaut que si vous êtes sûr de ce que vous faites.)
        """
        self.nb_lignes = size
        self.nb_blocs = 8
        self.lines = []
        self.setup()
        self.memory = memory
        self.perf_counter = 0
        self.perf_counter_cache = 0

    def setup(self):
        """
        Méthode de construction des lignes du cache.
        :return: None
        """
        for i in range(self.nb_lignes):
            l = Line_cache()
            self.lines.append(l)


    def write(self, address, data):
        """
        Ecrit la donnée à l'adresse correspondante.
        :param address: adresse
        :param data: donnée
        :return: None
        """
        # récupération des infos dans l'adresse
        tag, index, b = self.address_param(address)
        line = self.lines[index]
        if data < 0:
            data = (1 << 32) + data
        line.blocs[b] = data



    def read(self, address):
        """
        Lit la donnée correspondant à l'adresse.
        :param address: adresse
        :return: donnée
        """
        # récupération des informations dans l'addresse
        tag, index, b = self.address_param(address)

        line = self.lines[index]  # on récupère la ligne correspondant à l'index

        if line.valid == 0 or tag != line.tag:
            # si la ligne n'a pas encore été écrite ou ne correspond pas à l'info visée, alors on lit en rafale
            address_min = (tag << 7) + (index << 3)   # adresse du premier bloc
            line.blocs = self.memory.burst_read(address_min, self.nb_blocs)
            line.tag = tag

            # mesure de perf
            self.perf_counter_cache += 100
            self.perf_counter += 100
        else:
            self.perf_counter += 10
            self.perf_counter_cache += 100


        return line.blocs[b]


    def write_through(self, address, data):
        """
        Ecrit dans le cache et dans la mémoire la donnée à l'addresse fournie.
        :param address: adresse
        :param data: donnée
        :return: None
        """
        self.write(address, data)   # écriture dans le cache
        self.memory.write(address, data)    # écriture dans la mémoire

    def address_param(self, address):
        """
        Lit les différents paramètres de l'adresse
        :param address: adresse
        :return: tag, index, bloc
        """
        tag = (address & (0b111 << 7)) >> 7  # le tag correspond aux bits 7,8 et 9
        index = (address & (0b1111 << 3)) >> 3  # l'index correspond aux bits 3,4,5 et 6
        b = (address & 0b111)  # l'offset correspond aux bits 0,1 et 2

        return tag, index, b

    def __str__(self):
        s = "#"*50 + "\n"
        s += " ---------  CACHE  ---------  \n"
        s += "adresse" + " " + "tag".ljust(5, " ") + "valid "
        for i in range(self.nb_blocs):
            s += "Bloc " + str(i) + " "*6
        s += '\n'
        for i in range(self.nb_lignes):
            l = self.lines[i]
            s += str(hex(i)).ljust(8, ' ') + str(bin(l.tag)).ljust(5, " ") + str(l.valid).ljust(6, ' ')
            for j in range(self.nb_blocs):
                s += str(hex(l.blocs[j])).ljust(12, ' ')
            s += "\n"

        s += "#"*50
        return s



class Line_cache:
    """
    Classe modélisant une ligne de cache.
    On considère une ligne de données avec 8 blocs par lignes, donc un numéro de bloc / offset sur 3 bits,
    """

    def __init__(self):
        self.valid = 0
        self.tag = 0
        self.blocs = [0]*8


if __name__ == '__main__':
    mem = Storage()
    cache = Cache(mem)
    print(cache.address_param(95))