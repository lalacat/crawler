def fun_a():
    print("a")

test_a = lambda : fun_a()
test_b = lambda : fun_a()
a =fun_a

print(test_a)
print(test_b)
print(a)
print(fun_a)

