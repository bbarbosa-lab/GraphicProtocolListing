import tkinter as tk
from tkinter import scrolledtext
import psutil
from datetime import datetime


# =====================================================
# AVISO IMPORTANTE
# =====================================================
# Instale a biblioteca psutil antes de rodar o código.
#    pip install psutil
# 
# =====================================================


class CyberNetTerminal:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("C:\\> GRAPHIC PROTOCOL SCANNER v1.2 - DETECÇÃO DE AMEAÇAS")
        self.root.configure(bg="#0A0A0A")
        self.root.geometry("1320x760")
        self.root.resizable(True, True)

        # Área de saída do terminal
        self.output = scrolledtext.ScrolledText(
            self.root,
            bg="#0A0A0A",
            fg="#00FF41",  # Verde padrão
            font=("Courier New", 13, "bold"),
            insertbackground="#00FF41",
            wrap=tk.WORD,
            state="normal",
            relief="flat",
            borderwidth=0
        )
        self.output.pack(padx=12, pady=(12, 5), fill=tk.BOTH, expand=True)
        self.output.bind("<Key>", lambda e: "break")

        # ==================== CONFIGURAÇÃO DE CORES ====================
        self.output.tag_config("normal", foreground="#00FF41")  # Verde normal
        self.output.tag_config("red", foreground="#FF4444")  # Vermelho para ameaças
        self.output.tag_config("alert", foreground="#FFFF00")  # Amarelo para alertas

        # Frame do prompt
        input_frame = tk.Frame(self.root, bg="#0A0A0A")
        input_frame.pack(fill=tk.X, padx=12, pady=(0, 12))

        self.prompt_label = tk.Label(
            input_frame,
            text="C:\\> ",
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

    def print_line(self, text="", color="normal", end="\n"):
        """Imprime linha com cor personalizada"""
        self.output.insert(tk.END, text + end, color)
        self.output.see(tk.END)
        self.root.update_idletasks()

    def print_welcome(self):
        self.print_line("=" * 120, "normal")
        self.print_line(" " * 30 + "GRAPHIC PROTOCOL SCANNER v1.2", "normal")
        self.print_line(" " * 22 + "MONITOR DE CONEXÕES + DETECÇÃO DE AMEAÇAS", "normal")
        self.print_line(" " * 40 + "by Barbosa", "normal")
        self.print_line("=" * 120, "normal")
        self.print_line("")
        self.print_line("Ferramenta de análise de rede com detecção visual de ameaças.", "normal")
        self.print_line("Portas maliciosas aparecem em VERMELHO.", "alert")
        self.print_line("")
        self.print_line("Digite 'ajuda' para ver todos os comandos.", "normal")
        self.print_line("")

    def process_command(self, event=None):
        cmd = self.entry.get().strip()
        if not cmd:
            return

        self.print_line(f"C:\\> {cmd}", "normal")
        cmd_lower = cmd.lower()

        if cmd_lower in ["ajuda", "help"]:
            self.show_help()
        elif cmd_lower in ["conexoes", "netlist", "connections", "lista", "scan"]:
            self.show_connections()
        elif cmd_lower in ["maliciosos", "suspicious", "ameacas"]:
            self.show_malicious_protocols()
        elif cmd_lower in ["refresh", "atualizar"]:
            self.print_line("\nAtualizando lista de conexões...\n", "normal")
            self.show_connections()
        elif cmd_lower in ["sobre", "about"]:
            self.show_about()
        elif cmd_lower in ["limpar", "cls", "clear"]:
            self.output.delete(1.0, tk.END)
            self.print_welcome()
        elif cmd_lower in ["sair", "exit", "quit"]:
            self.print_line("\nEncerrando o Graphic Protocol Scanner... Até a próxima!", "normal")
            self.root.after(900, self.root.quit)
            return
        else:
            self.print_line(f"Erro: Comando '{cmd}' não reconhecido.", "normal")
            self.print_line("Digite 'ajuda' para ver os comandos.", "normal")

        self.entry.delete(0, tk.END)

    def show_help(self):
        self.print_line("""
COMANDOS DISPONÍVEIS
====================
  ajuda              → Mostra esta ajuda
  conexoes / lista   → Lista todas as conexões (portas maliciosas em VERMELHO)
  maliciosos         → Lista de portas e protocolos suspeitos
  refresh            → Atualiza a lista de conexões
  sobre              → Sobre o Graphic Protocol Scanner
  limpar / cls       → Limpa a tela
  sair / exit        → Fecha o terminal
""", "normal")

    def show_malicious_protocols(self):
        self.print_line("=" * 100, "normal")
        self.print_line(" " * 25 + "PORTAS E PROTOCOLOS FREQUENTEMENTE MALICIOSOS", "normal")
        self.print_line("=" * 100, "normal")
        self.print_line("")
        self.print_line("PORTA     PROTOCOLO          USO COMUM EM MALWARE", "normal")
        self.print_line("-" * 75, "normal")

        malicious = [
            ("4444", "TCP", "Metasploit, Cobalt Strike, Reverse Shell"),
            ("1337", "TCP", "Leet / Backdoors"),
            ("8080", "TCP", "Proxy Reverso / C2 Servers"),
            ("9999", "TCP", "Vários RATs e Trojans"),
            ("31337", "TCP", "Back Orifice"),
            ("3389", "TCP", "RDP - Brute Force"),
            ("445", "TCP", "SMB - Ransomware / EternalBlue"),
            ("22", "TCP", "SSH - Brute Force"),
            ("53", "UDP", "DNS Tunneling"),
            ("6666", "TCP", "IRC Bots / C2"),
            ("3333", "TCP", "Crypto Miners"),
        ]

        for port, proto, desc in malicious:
            self.print_line(f"{port:<9} {proto:<6}   {desc}", "normal")

        self.print_line("")
        self.print_line("→ Quando uma dessas portas aparecer em 'conexoes', a linha ficará VERMELHA.", "alert")

    def show_connections(self):
        self.print_line(f"[{datetime.now().strftime('%H:%M:%S')}] Analisando conexões de rede...\n", "normal")

        try:
            connections = psutil.net_connections(kind='inet')

            self.print_line("=" * 145, "normal")
            self.print_line(
                f"{'PROTO':<6} {'LOCAL':<28} {'REMOTO (DESTINO)':<35} {'DIR':<8} {'STATUS':<12} {'PID':<6} PROCESSO",
                "normal")
            self.print_line("=" * 145, "normal")

            suspicious_count = 0
            malicious_ports = {"4444", "1337", "8080", "9999", "31337", "3389", "445", "6666", "3333", "14444"}

            for conn in connections:
                proto = "TCP" if conn.type == 1 else "UDP"

                local = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "*:*"
                remote = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "*:*"

                direction = "OUT" if conn.raddr else "IN/LISTEN"
                status = conn.status if conn.status else "N/A"
                pid = conn.pid if conn.pid is not None else "-"

                # Nome do processo
                if pid != "-" and pid != -1:
                    try:
                        proc_name = psutil.Process(pid).name()
                    except:
                        proc_name = "???"
                else:
                    proc_name = "N/A"

                line = f"{proto:<6} {local:<28} {remote:<35} {direction:<8} {status:<12} {str(pid):<6} {proc_name}"

                # ==================== DETECÇÃO DE PORTA MALICIOSA ====================
                is_suspicious = False
                if conn.raddr:
                    remote_port = str(conn.raddr.port)
                    if remote_port in malicious_ports:
                        is_suspicious = True
                        suspicious_count += 1

                if is_suspicious:
                    self.print_line(line + "   [!] MALICIOSO", "red")
                else:
                    self.print_line(line, "normal")

            self.print_line("=" * 145, "normal")
            self.print_line(f"Total de conexões: {len(connections)}", "normal")

            if suspicious_count > 0:
                self.print_line(f"⚠️  {suspicious_count} CONEXÃO(ÕES) MALICIOSA(S) DETECTADA(S)!", "red")
            else:
                self.print_line("Nenhuma conexão maliciosa detectada no momento.", "normal")

        except Exception as e:
            self.print_line(f"ERRO: {e}", "red")
            self.print_line("Certifique-se de que psutil está instalado (pip install psutil).", "normal")

    def show_about(self):
        self.print_line("""
SOBRE O GRAPHIC PROTOCOL SCANNER v1.2
=====================================
Ferramenta desenvolvida em Python + Tkinter
Estilo terminal retro 90's com detecção visual de ameaças.

Funcionalidades:
• Monitoramento em tempo real de conexões TCP/UDP
• Identificação do processo de origem
• Detecção automática de portas maliciosas
• Linhas em VERMELHO quando ameaça é detectada

Ideal para portfólio de Cibersegurança / Blue Team / Threat Hunting.
""", "normal")


if __name__ == "__main__":
    app = CyberNetTerminal()
    app.root.mainloop()
