class Singleton(object):
    def __init__(self,name):
        self.name = name

    def __new__(cls, *args, **kwargs):

        if not hasattr(cls,"instance"):
            cls.instance = super(Singleton,cls).__new__(cls)
        return cls.instance


s1 = Singleton("a")
s2 = Singleton("b")

print(s1.name)
print(s2.name)