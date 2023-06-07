messagens = []
with open('mensagens.txt', 'r') as file:
    while True:
        a = file.readline().rstrip('\n')
        if a == '':
            break
        b = a.split(',,')
        obj = {'name': b[0], 'message': b[1]}
        messagens.append(obj)
print(messagens)