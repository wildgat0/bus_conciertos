import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('147.185.238.111', username='root', password='JoseIgnacioLeightonZavala98', timeout=10)

docker_repo = "deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu noble stable"

commands = [
    "apt-get update -q",
    "apt-get install -y -q ca-certificates curl gnupg",
    "install -m 0755 -d /etc/apt/keyrings",
    "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg",
    "chmod a+r /etc/apt/keyrings/docker.gpg",
    f"echo '{docker_repo}' > /etc/apt/sources.list.d/docker.list",
    "apt-get update -q",
    "apt-get install -y -q docker-ce docker-ce-cli containerd.io docker-compose-plugin",
    "docker --version && docker compose version",
]

for cmd in commands:
    label = cmd[:70] + "..." if len(cmd) > 70 else cmd
    print(f">> {label}")
    stdin, stdout, stderr = client.exec_command(cmd, timeout=120)
    out = stdout.read().decode().strip()
    err = stderr.read().decode().strip()
    if out:
        print(out)
    if err and "WARNING" not in err and "warning" not in err and "NOTICE" not in err:
        print(f"STDERR: {err[:300]}")

client.close()
print("\nDONE")
