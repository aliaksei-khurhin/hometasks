f=open('./access.log')
d={}
for line in f:
    pars=line.split(" ")
    d[pars[0]]=d.get(pars[0],0) +1
e=sorted(d, key=d.__getitem__, reverse=True)
print (e[:10])