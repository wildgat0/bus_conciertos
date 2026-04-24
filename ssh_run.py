import paramiko, sys

def ssh_run(cmd, timeout=120):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('147.185.238.111', username='root', password='JoseIgnacioLeightonZavala98', timeout=10)
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    err = stderr.read().decode('utf-8', errors='replace').strip()
    client.close()
    return out, err

if __name__ == '__main__':
    cmd = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else 'echo ok'
    out, err = ssh_run(cmd)
    if out:
        print(out.encode('ascii', errors='replace').decode())
    if err:
        print("STDERR:", err.encode('ascii', errors='replace').decode()[:500])
