from Animal import Animal


class Fish(Animal):
    def __init__(self):
        self.have_gills = True
        super().__init__()

    def Breathe(self):
        super().Breathe()
        print("Under water")


fish1 = Fish()
fish1.Breathe()

