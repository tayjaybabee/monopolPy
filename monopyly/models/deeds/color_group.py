


class ColorGroup:
    def __init__(self, color_name: str, total_properties: int = 3):
        self.__color_name = None
        self.__total_properties = None

        self.color_name = color_name
        self.total_properties = total_properties

        self.__deeds = []