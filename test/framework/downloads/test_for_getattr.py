class A(object):
    def __init__(self):
        self.a = "aa"
        self.b = None
        self.abc = {}
aa = A()
default_a = "abc"
d = getattr(aa,"a",default_a)
d2 = getattr(aa,"b",default_a)
d3 = getattr(aa,"c",default_a)
deb = "ccc"
d4 = aa.abc.get("aaa",deb)
d5 = aa.abc.get("ccc","ggg")
d6 = aa.abc.get("ddd","fff")
print("d",d)
print("d2",d2)
print("d3",d3)
print("d4",d4)
print("d5",d5)
print("d6",d6)

maxnum = 1212
expect = 132
# 哪个小取值哪个，90 and -1 = -1 ，0 and -1 = 0
a = maxnum and expect
print(a)