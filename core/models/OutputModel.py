
class OutputModel:

    def __init__(self, trajet):
        self.trajet = trajet

    def generateFile(self, outputPath: str):
        pass

    def compile(self) -> str:
        """Retourne la string complète du fichier d'output en fonction du trajet donné dans init

        Returns:
            str: String de sortie normalisée
        """
        out = ""

        for row in self.trajet:
            
            for ballon in row:
                out += str(ballon) + " "
            out += "\n"
        return out