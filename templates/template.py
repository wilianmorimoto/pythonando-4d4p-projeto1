import sys
import os
sys.path.append(os.path.abspath(os.curdir))
from views.password_views import FernetHasher
from model.password import Password


action = input('[ 1 ] Salvar nova senha\n[ 2 ] Ver uma senha salva\n')

match action:
    case '1':
        if len(Password.get()) == 0:
            key, path = FernetHasher.create_key(archive=True)
            print('Sua chave foi criada com sucesso, salve-a com cuidado!')
            print(f'Chave: {key.decode('utf-8')}')
            if path:
                print('Chave salva no arquivo, lembre-se de remover o arquivo após transferir de local.')
                print(f'Caminho: {path}')
        else:
            key = input('Digite sua chave usada para criptografia, use sempre a mesma chave: ')
        domain = input('Domínio: ')
        password = input('Senha: ')
        fernet_user = FernetHasher(key)
        p1 = Password(domain=domain, password=fernet_user.encrypt(password).decode('utf-8'))
        p1.save()
    case '2':
        domain = input('Domínio: ')
        key = input('Key: ')
        fernet_user = FernetHasher(key)
        data = Password.get()
        for i in data:
            if domain in i['domain']:
                password = fernet_user.decrypt(i['password'])
        if password:
            print(f'Sua senha: {password}')
        else:
            print('Nenhuma senha encontrada para o domínio.')