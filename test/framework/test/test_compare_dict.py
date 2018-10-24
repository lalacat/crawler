A = {'a','b','c'}
Aa = {'b','c'}
Ab = {'a','b','c','d'}
B = {'b','c','d'}

if A <= Aa:
    print("A<Aa")
elif A > Aa:
    print("A>Aa")


if A <= Ab:
    print("A<Aa")
elif A > Ab:
    print("A>Aa")
else:
    print('A与Ab无法比较')

if A <= B:
    print("A<Aa")
elif A > B:
    print("A>Aa")
else:
    print('A与B无法比较')
