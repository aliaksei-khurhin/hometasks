test='qwertrewq'

if test[:(len(test)//2)] == test[len(test):(len(test)//2):-1]:
    print ('Word is polindrom')
else:
    print ("Word isn't a polindrom")