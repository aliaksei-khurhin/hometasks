keys = ['a', 'b', 'c', 'd', 'e']
val = [1, 2, 3, 5]

d = {}

def function (keys,val,d):
    for i in range(len(keys)):
        if i < len(val):
            d[keys[i]] = val[i]
        else:
            d[keys[i]] = 'none'
    return (d)

function(keys,val,d)
print(d)