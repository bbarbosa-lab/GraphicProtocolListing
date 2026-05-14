import tkinter as tk
from tkinter import scrolledtext
import psutil
from datetime import datetime


# =====================================================
# AVISO IMPORTANTE
# =====================================================
# Execute antes de rodar o programa:
#    pip install psutil
# =====================================================


class CyberNetTerminal:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("C:\\CYBER> CYBERNET SCANNER v1.1 - PORTFÓLIO CIBERSEGURANÇA")
        self.root.configure(bg="#0A0A0A")
        self.root.geometry("1250x740")
        self.root.resizable(True, True)

        # Área de saída do terminal
        self.output = scrolledtext.ScrolledText(
            self.root,
            bg="#0A0A0A",
            fg="#00FF41",
            font=("Courier New", 13, "bold"),
            insertbackground="#00FF41",
            wrap=tk.WORD,
            state="normal",
            relief="flat",
            borderwidth=0
        )
        self.output.pack(padx=12, pady=(12, 5), fill=tk.BOTH, expand=True)
        self.output.bind("<Key>", lambda e: "break")

        # Frame do prompt
        input_frame = tk.Frame(self.root, bg="#0A0A0A")
        input_frame.pack(fill=tk.X, padx=12, pady=(0, 12))

        self.prompt_label = tk.Label(
            input_frame,
            text="C:\\CYBER> ",
            bg="#0A0A0A",
            fg="#00FF41",
            font=("Courier New", 13, "bold")
        )
        self.prompt_label.pack(side=tk.LEFT)

        self.entry = tk.Entry(
            input_frame,
            bg="#0A0A0A",
            fg="#00FF41",
            insertbackground="#00FF41",
            font=("Courier New", 13, "bold"),
            borderwidth=0,
            highlightthickness=0
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.focus_set()

        self.entry.bind("<Return>", self.process_command)

        self.print_welcome()

    def print_line(self, text="", end="\n"):
        self.output.insert(tk.END, text + end)
        self.output.see(tk.END)
        self.root.update_idletasks()

    def print_welcome(self):
        self.print_line("=" * 110)
        self.print_line(" " * 28 + "CYBERNET SCANNER v1.1")
        self.print_line(" " * 20 + "MONITOR DE CONEXÕES + DETECÇÃO DE AMEAÇAS")
        self.print_line(" " * 35 + "by Gothic")
        self.print_line("=" * 110)
        self.print_line("")
        self.print_line("Ferramenta de análise de rede para portfólio de Cibersegurança.")
        self.print_line("")
        self.print_line("Digite 'ajuda' para ver todos os comandos.")
        self.print_line("")

    def process_command(self, event=None):
        cmd = self.entry.get().strip()
        if not cmd:
            return

        self.print_line(f"C:\\CYBER> {cmd}")
        cmd_lower = cmd.lower()

        if cmd_lower in ["ajuda", "help"]:
            self.show_help()
        elif cmd_lower in ["conexoes", "netlist", "connections", "lista", "scan"]:
            self.show_connections()
        elif cmd_lower in ["maliciosos", "suspicious", "ameacas"]:
            self.show_malicious_protocols()
        elif cmd_lower in ["refresh", "atualizar"]:
            self.print_line("\nAtualizando lista de conexões...\n")
            self.show_connections()
        elif cmd_lower in ["sobre", "about"]:
            self.show_about()
        elif cmd_lower in ["limpar", "cls", "clear"]:
            self.output.delete(1.0, tk.END)
            self.print_welcome()
        elif cmd_lower in ["sair", "exit", "quit"]:
            self.print_line("\nEncerrando o CyberNet Scanner... Até a próxima!")
            self.root.after(900, self.root.quit)
            return
        else:
            self.print_line(f"Erro: Comando '{cmd}' não reconhecido.")
            self.print_line("Digite 'ajuda' para ver os comandos.")

        self.entry.delete(0, tk.END)

    def show_help(self):
        self.print_line("""
COMANDOS DISPONÍVEIS
====================
  ajuda              → Mostra esta ajuda
  conexoes / lista   → Lista todas as conexões de rede (com processo)
  maliciosos         → Lista protocolos/ports suspeitos ou maliciosos
  refresh            → Atualiza a lista de conexões
  sobre              → Sobre o CyberNet Scanner
  limpar / cls       → Limpa a tela
  sair / exit        → Fecha o terminal
""")

    def show_malicious_protocols(self):
        """Lista de protocolos e portas frequentemente associadas a ameaças"""
        self.print_line("=" * 95)
        self.print_line(" " * 20 + "PROTOCOLOS E PORTAS FREQUENTEMENTE MALICIOSAS")
        self.print_line("=" * 95)
        self.print_line("")
        self.print_line("PORTA     PROTOCOLO          USO COMUM EM MALWARE")
        self.print_line("-" * 70)

        malicious = [
            ("4444", "TCP", "Metasploit, Cobalt Strike, Reverse Shell"),
            ("1337", "TCP", "Leet (comum em backdoors)"),
            ("8080", "TCP", "Proxy reverso / C2 Servers"),
            ("9999", "TCP", "Vários RATs e trojans"),
            ("31337", "TCP", "Back Orifice / elite hacker ports"),
            ("3389", "TCP", "RDP - frequentemente brute forced"),
            ("445", "TCP", "SMB - EternalBlue / ransomware"),
            ("22", "TCP", "SSH - brute force attacks"),
            ("53", "UDP", "DNS Tunneling (exfiltração)"),
            ("123", "UDP", "NTP Amplification"),
            ("25", "TCP", "SMTP - Spam / Phishing"),
            ("6666", "TCP", "IRC Bots / C2"),
            (" mining ports", "", "3333, 3334, 14444 (Crypto Miners)")
        ]

        for port, proto, desc in malicious:
            self.print_line(f"{port:<9} {proto:<6}   {desc}")

        self.print_line("")
        self.print_line("Dica: Use 'conexoes' e procure por estas portas.")

    def show_connections(self):
        """Lista todas as conexões com ênfase em processo e direção"""
        self.print_line(f"[{datetime.now().strftime('%H:%M:%S')}] Obtendo conexões de rede...\n")

        try:
            connections = psutil.net_connections(kind='inet')

            self.print_line("=" * 135)
            self.print_line(
                f"{'PROTO':<6} {'LOCAL':<28} {'REMOTO (DESTINO)':<32} {'DIREÇÃO':<9} {'STATUS':<12} {'PID':<6} PROCESSO")
            self.print_line("=" * 135)

            for conn in connections:
                proto = "TCP" if conn.type == 1 else "UDP"

                local = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "*:*"
                remote = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "*:*"

                # Determina direção
                direction = "OUT" if conn.raddr else "IN/LISTEN"

                status = conn.status if conn.status else "N/A"
                pid = conn.pid if conn.pid is not None else "-"

                # Nome do processo (de onde está saindo a conexão)
                if pid != "-" and pid != -1:
                    try:
                        proc_name = psutil.Process(pid).name()
                    except:
                        proc_name = "???"
                else:
                    proc_name = "N/A"

                # Destaca conexões suspeitas (exemplo simples)
                suspicious = " [!]" if remote != "*:*" and any(p in remote for p in ["4444", "1337", "8080"]) else ""

                line = f"{proto:<6} {local:<28} {remote:<32} {direction:<9} {status:<12} {str(pid):<6} {proc_name}{suspicious}"
                self.print_line(line)

            self.print_line("=" * 135)
            self.print_line(f"Total de conexões: {len(connections)}")
            self.print_line("Use 'maliciosos' para ver portas perigosas comuns.")

        except Exception as e:
            self.print_line(f"ERRO: {e}")
            self.print_line("Certifique-se de que psutil está instalado.")

    def show_about(self):
        self.print_line("""
SOBRE O CYBERNET SCANNER v1.1
=============================
Ferramenta desenvolvida em Python + Tkinter
Estilo terminal retro 90's.

Funcionalidades:
• Monitoramento em tempo real de conexões TCP/UDP
• Identificação clara do processo de origem
• Detecção visual de conexões de saída
• Lista de protocolos maliciosos

Perfeito para portfólio de:
Blue Team • SOC • Threat Hunting • Cibersegurança
""")


if __name__ == "__main__":
    app = CyberNetTerminal()
    app.root.mainloop()