class Reader:
    def __init__(self, path):
        self.path = path

    def readFile(self):
        with open(self.path) as f:
            content = f.readlines()
            # Abro el archivo para las H posicionadas
        content = [x.split() for x in content]
        # Seteo los arrays en una variable llamada content de tipo array
        temp = [0] * len(content)

        for i in range(0, len(content)):
            for j in range(0, len(content[i])):
                if content[i][j] == 'H':
                    temp[j] = i
        # Realizo un for para una matriz bidimensional
        return temp
