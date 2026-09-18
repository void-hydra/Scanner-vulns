import socket
import subprocess
import sys
import os
import json

banner = r"""
⠀⠀⠀⠀⠀⢸⠓⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢸⠀⠀⠑⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢸⡆⠀⠀⠀⠙⢤⡷⣤⣦⣀⠤⠖⠚⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣠⡿⠢⢄⡀⠀⡇⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠸⠷⣶⠂⠀⠀⠀⣀⣀⠀⠀⠀
⢸⣃⠀⠀⠉⠳⣷⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠉⠉⠉⢉⡭⠋
⠀⠘⣆⠀⠀⠀⠁⠀⢀⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠋⠀⠀
⠀⠀⠘⣦⠆⠀⠀⢀⡎⢹⡀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⡀⣠⠔⠋⠀⠀⠀⠀As sombras me perseguem - gengar
⠀⠀⠀⡏⠀⠀⣆⠘⣄⠸⢧⠀⠀⠀⠀⢀⣠⠖⢻⠀⠀⠀⣿⢥⣄⣀⣀⣀⠀ Voce tem medo do escuro? eu vivo nele. - gengar
⠀⠀⢸⠁⠀⠀⡏⢣⣌⠙⠚⠀⠀⠠⣖⡛⠀⣠⠏⠀⠀⠀⠇⠀⠀⠀⠀⢙⣣⠄
⠀⠀⢸⡀⠀⠀⠳⡞⠈⢻⠶⠤⣄⣀⣈⣉⣉⣡⡔⠀⠀⢀⠀⠀⣀⡤⠖⠚⠀⠀
⠀⠀⡼⣇⠀⠀⠀⠙⠦⣞⡀⠀⢀⡏⠀⢸⣣⠞⠀⠀⠀⡼⠚⠋⠁⠀⠀⠀⠀⠀
⠀⢰⡇⠙⠀⠀⠀⠀⠀⠀⠉⠙⠚⠒⠚⠉⠀⠀⠀⠀⡼⠁⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢧⡀⠀⢠⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠙⣶⣶⣿⠢⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠉⠀⠀⠀⠙⢿⣳⠞⠳⡄⠀⠀⠀⢀⡞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀⠹⣄⣀⡤⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

print("feito por: void")
print("scanner de vuln focado para bug bounty")
print(" este simples scanner contem: SQLMAP,NUCLEI,SHODAN e uma ferramenta portscanning so com portas vulneraveis feitas por mim")
print("um salve pro: hydra ")
print("bug bounty é lindo...")
print(banner)

portas_str = (
    "80 - http, 443 - https, 22 - ssh, 23 - telnet, 3389 - rdp, "
    "135 - msrpc, 139 - netbios, 145 - ms-sna-server, 3306 - mysql, "
    "5432 - postgresql, 1433 - mssql, 1527 - oracle-tns, 27 - imaps, "
    "1900 - ssdp, 111 - rpcbind, 161 - snmp, 6200 - oracle-ons, "
    "162 - snmptrap, 21 - ftp, 5900 - vnc, 5985 - winrm, 5986 - winrm-https, "
    "4444 - metasploit, 10000 - webmin, 1434 - mssql-browser, 1521 - oracle, "
    "6379 - redis, 9200 - elasticsearch, 27017 - mongodb"
)

portas = {}
for item in portas_str.split(", "):
    num, nome = item.split(" - ")
    portas[int(num)] = nome


def portscan(host):
    abertas = []
    print(f"\n[*] Portscan iniciando em {host} ...\n")
    for porta, nome in portas.items():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        resultado = s.connect_ex((host, porta))
        if resultado == 0:
            print(f'  [ABERTA]  Porta {porta} ({nome})')
            abertas.append((porta, nome))
        else:
            print(f'  [FECHADA] Porta {porta} ({nome})')
        s.close()
    return abertas


def run_nuclei(host, portas_abertas):
    print("\n" + "=" * 50)
    print("[*] Nuclei executando ...")
    print("=" * 50)

    port_list = ",".join(str(p) for p, _ in portas_abertas)
    https_flag = any(p == 443 for p, _ in portas_abertas)

    if https_flag:
        url_proto = "https"
        output_file = f"nuclei_{host}_https.txt"
    else:
        url_proto = "http"
        output_file = f"nuclei_{host}.txt"

    cmd = [
        "nuclei",
        "-u", f"{url_proto}://{host}",
        "-p", port_list,
        "-severity", "medium,high,critical",
        "-o", output_file,
        "-silent"
    ]

    try:
        result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=300)
        print(f"\n[+] Nuclei relatório salvo em: {output_file}")
    except FileNotFoundError:
        print("[-] nuclei não encontrado. Instale: go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest")
    except subprocess.TimeoutExpired:
        print("[-] Nuclei timeout (300s)")
    except subprocess.CalledProcessError as e:
        print(f"[-] erro ao executar nuclei: {e}")


def run_sqlmap(host, portas_abertas):
    web_ports = [p for p, _ in portas_abertas if p in (80, 443, 8080, 8443)]
    if not web_ports:
        print("\n[*] Nenhuma porta web aberta, sqlmap será pulado.")
        return

    print("\n" + "=" * 50)
    print("[*] SQLMap executando ...")
    print("=" * 50)

    for porta in web_ports:
        scheme = "https" if porta == 443 else "http"
        url = f"{scheme}://{host}"
        cmd = [
            "sqlmap",
            "-u", url,
            "--batch",
            "--random-agent",
            "--level", "2",
            "--risk", "1",
            "--output-dir", f"sqlmap_{host}_{porta}"
        ]
        print(f"\n[*] Testando: {url}")
        try:
            result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=600)
        except FileNotFoundError:
            print("[-] sqlmap não encontrado. Instale: pip install sqlmap")
            break
        except subprocess.TimeoutExpired:
            print(f"[-] sqlmap timeout na porta {porta}")
        except subprocess.CalledProcessError as e:
            print(f"[-] erro ao executar sqlmap na porta {porta}: {e}")


def run_shodan_cves(host):
    print("\n" + "=" * 50)
    print("[*] Shodan CVE lookup ...")
    print("=" * 50)

    try:
        import shodan
    except ImportError:
        print("[-] shodan não instalado. Rode: pip install shodan")
        return

    api_key = os.environ.get("SHODAN_API_KEY")
    if not api_key:
        print("[-] SHODAN_API_KEY não definida. Exporte: export SHODAN_API_KEY='sua_chave'")
        return

    try:
        sh = shodan.Shodan(api_key)
        data = sh.host(host)
        vulns = data.get("vulns", [])

        if not vulns:
            print(f"[*] Nenhum CVE encontrado para {host} no Shodan.")
        else:
            print(f"\n[+] {len(vulns)} CVE(s) encontrados para {host}:\n")
            for v in vulns:
                cve_id = v.get("id", "N/A")
                description = v.get("description", "N/A")[:100]
                print(f"  CVE: {cve_id}")
                print(f"  Desc: {description}...")
                print()

            with open(f"shodan_cves_{host}.json", "w") as f:
                json.dump(vulns, f, indent=2)
            print(f"[+] Relatório salvo em: shodan_cves_{host}.json")

    except Exception as e:
        print(f"[-] Erro: {e}")

if __name__ == "__main__":
    host = input("Qual é o IP target ? ").strip()

    if not host:
        print("[-] IP inválido.")
        sys.exit(1)

    try:
        socket.inet_aton(host)
    except socket.error:
        print("[-] IP inválido.")
        sys.exit(1)

    abertas = portscan(host)

    if not abertas:
        print("\n[-] Nenhuma porta aberta. Encerrando.")
        sys.exit(0)

    run_nuclei(host, abertas)
    run_sqlmap(host, abertas)
    run_shodan_cves(host)

    print("\n" + "=" * 50)
    print("[+] Scan concluído!")
    print("=" * 50)
