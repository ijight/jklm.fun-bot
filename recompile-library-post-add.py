f = open('dict.txt', 'r')
var = f.read()
f.close()
print("Completed opening")
#Alphabatize and uppercase all
var = var.upper()
var = var.split('\n')
var.sort()
print("Completed string to list")
#remove duplicates
var = list(dict.fromkeys(var))
print('Removed duplicates')
#recompile string
var = '\n'.join([str(elem) for elem in var])
print('Remade string')

f= open("dict.txt","w")
f.write(var)
f.close()
print('Completed file')