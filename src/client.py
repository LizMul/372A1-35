import socket, os

HOST = '127.0.0.1'
PORT = 50007

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    f = s.makefile('rwb')
    while True:
        try: line = input().strip()
        except: line = 'QUIT'
        if not line: continue
        if line.upper().startswith('FILE '):
            path = line.split(' ', 1)[1]
            try:
                with open(path, 'rb') as fp: blob = fp.read()
            except: continue
            name = os.path.basename(path)
            header = f'FILE {name} {len(blob)}\n'.encode()
            f.write(header + blob)
            f.flush()
            reply = f.readline()
            if not reply:
                break
            print(reply.decode().strip())
            continue 

        f.write((line + '\n').encode())
        f.flush()
        reply = f.readline()
        if not reply:
            break
        print(reply.decode().strip())
        if line.upper().startswith('QUIT'):
            break