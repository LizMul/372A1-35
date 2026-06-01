import socket
import os

HOST = '127.0.0.1'
PORT = 50007
USERS_FILE = 'users.txt'
with open(USERS_FILE) as uf:
    USERS = {line.strip() for line in uf if line.strip()}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    while True:
        conn, addr = s.accept()
        with conn:
            try:
                f = conn.makefile('rwb')
                user = None
                while True:
                    line = f.readline()
                    if not line: break
                    parts = line.decode().strip().split(' ')
                    cmd = parts[0].upper()
                    arg = '' if len(parts) < 2 else " ".join(parts[1:])
                    if cmd =='LOGIN': 
                        if arg in USERS:
                            user = arg
                            print(f'{user} has logged in')
                            f.write(b'OK\n')
                        else:
                            f.write(b'TRY AGAIN\n')
                    elif cmd == 'MSG':
                        if not user or not arg:
                            f.write(b'TRY AGAIN\n')
                        else:
                            print(f'{user}: {arg}')
                            f.write(b'OK\n')

                    
                    elif cmd == 'FILE':
                        pass


                    elif cmd == 'QUIT':
                        f.write(b'BYE\n')
                        f.flush()
                        break
                    else:
                        f.write(b'TRY AGAIN\n')
                    f.flush()
            except:
                print('ERROR')




            
        
