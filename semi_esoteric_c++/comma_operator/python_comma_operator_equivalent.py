

def f():
    print "inside f"

def f_bool():
    print "inside f"
    return False

    
_, i = f(), 4
print i

i = f() or 4
print i

i = f_bool() or 4
print i

i = f()
print i
