import socket
import os

HOST = '127.0.0.1'
PORT = 50007
HERE = os.path.dirname(__file__)
USERS_FILE = os.path.join(HERE, 'users.txt')
RECEIVE_DIR = os.path.join(HERE, 'received_files')

os.makedirs(RECEIVE_DIR, exist_ok=True)

with open(USERS_FILE) as uf:
    USERS = {line.strip() for line in uf if line.strip()}


def start_server(host=HOST, port=PORT, users=USERS, receive_dir=RECEIVE_DIR):
    os.makedirs(receive_dir, exist_ok=True)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(1)
        while True:
            conn, addr = s.accept()
            with conn:
                try:
                    f = conn.makefile('rwb')
                    user = None
                    while True:
                        line = f.readline()
                        if not line:
                            print('Client disconnected')
                            break
                        parts = line.decode().strip().split(' ')
                        cmd = parts[0].upper()
                        arg = '' if len(parts) < 2 else ' '.join(parts[1:])
                        if cmd == 'LOGIN':
                            if arg in users:
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
                            if not user or not arg:
                                f.write(b'TRY AGAIN\n')
                            else:
                                header_parts = arg.split(' ')
                                if len(header_parts) < 2:
                                    f.write(b'TRY AGAIN\n')
                                else:
                                    filename = os.path.basename(header_parts[0])
                                    try:
                                        size = int(header_parts[1])
                                    except ValueError:
                                        size = -1
                                    if not filename or size < 0:
                                        f.write(b'TRY AGAIN\n')
                                    else:
                                        print(f'Receiving file from {user}: {filename} ({size} bytes)')
                                        content = f.read(size)
                                        if len(content) != size:
                                            print(f'ERROR: expected {size} bytes, got {len(content)} bytes')
                                            f.write(b'ERROR\n')
                                        else:
                                            path = os.path.join(receive_dir, filename)
                                            with open(path, 'wb') as out_file:
                                                out_file.write(content)
                                            print(f'File received: {path}')
                                            f.write(b'OK\n')
                        elif cmd == 'QUIT':
                            f.write(b'BYE\n')
                            f.flush()
                            break
                        else:
                            f.write(b'TRY AGAIN\n')
                        f.flush()
                except Exception as e:
                    print('ERROR', e)


if __name__ == '__main__':
    start_server()




            
        
