import os
import shutil
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
import time
from datetime import datetime

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class NodeKnife:
    def __init__(self):
        self.total_removido = 0
        self.total_tamanho = 0
        self.erros = []
        self.lock = threading.Lock()
        self.pastas_encontradas = []
        
    def banner(self):
        banner_art = f"""
{Colors.CYAN}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ███╗   ██╗ ██████╗ ██████╗ ███████╗                   ║
║   ████╗  ██║██╔═══██╗██╔══██╗██╔════╝                   ║
║   ██╔██╗ ██║██║   ██║██║  ██║█████╗                     ║
║   ██║╚██╗██║██║   ██║██║  ██║██╔══╝                     ║
║   ██║ ╚████║╚██████╔╝██████╔╝███████╗                   ║
║   ╚═╝  ╚═══╝ ╚═════╝ ╚═════╝ ╚══════╝                   ║
║                                                           ║
║   ██╗  ██╗███╗   ██╗██╗███████╗███████╗                 ║
║   ██║ ██╔╝████╗  ██║██║██╔════╝██╔════╝                 ║
║   █████╔╝ ██╔██╗ ██║██║█████╗  █████╗                   ║
║   ██╔═██╗ ██║╚██╗██║██║██╔══╝  ██╔══╝                   ║
║   ██║  ██╗██║ ╚████║██║██║     ███████╗                 ║
║   ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚═╝     ╚══════╝                 ║
║                                                           ║
║        🔪 Limpador Avançado de node_modules 🔪           ║
║                  v2.0 - Turbo Edition                    ║
╚═══════════════════════════════════════════════════════════╝
{Colors.ENDC}"""
        print(banner_art)
        
    def calcular_tamanho(self, pasta):
        """Fazendo umas continhas aqui pra ver o tamanho dessa bagunça"""
        total = 0
        try:
            for dirpath, _, filenames in os.walk(pasta):
                for f in filenames:
                    try:
                        fp = os.path.join(dirpath, f)
                        total += os.path.getsize(fp)
                    except (FileNotFoundError, PermissionError, OSError):
                        pass
        except Exception:
            pass
        return total / (1024 * 1024)  # MB
    
    def formatar_tamanho(self, tamanho_mb):
        """Deixando esses números mais bonitinhos pra vocês entenderem"""
        if tamanho_mb >= 1024:
            return f"{tamanho_mb / 1024:.2f} GB"
        return f"{tamanho_mb:.2f} MB"
    
    def buscar_node_modules(self, diretorio_base):
        """Aqui que a gente busca esses lixos de node_modules espalhados por aí"""
        print(f"\n{Colors.YELLOW}⏳ Escaneando diretórios...{Colors.ENDC}")
        print(f"{Colors.CYAN}📂 Base: {diretorio_base}{Colors.ENDC}\n")
        
        pastas = []
        try:
            for raiz, dirs, _ in os.walk(diretorio_base, topdown=True):
                # Ignorando essas pastas chatas do sistema, não queremos causar
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['$RECYCLE.BIN', 'System Volume Information']]
                
                if 'node_modules' in dirs:
                    caminho_completo = os.path.join(raiz, 'node_modules')
                    pastas.append(caminho_completo)
                    print(f"{Colors.GREEN}✓{Colors.ENDC} Encontrado: {caminho_completo}")
                    # Não entramos dentro da node_modules senão travamos aqui até 2030
                    dirs.remove('node_modules')
        except PermissionError:
            pass
            
        return pastas
    
    def remover_pasta(self, caminho):
        """Aqui é onde a mágica acontece - deletando essa porcaria toda"""
        try:
            tamanho = self.calcular_tamanho(caminho)
            
            print(f"\n{Colors.BLUE}{'='*60}{Colors.ENDC}")
            print(f"{Colors.BOLD}🗑️  Removendo:{Colors.ENDC} {caminho}")
            print(f"{Colors.YELLOW}📦 Tamanho:{Colors.ENDC} {self.formatar_tamanho(tamanho)}")
            
            # Fazendo uma animaçãozinha marota enquanto apaga tudo
            print(f"{Colors.CYAN}⚡ Processando", end="", flush=True)
            for _ in range(3):
                time.sleep(0.2)
                print(".", end="", flush=True)
            
            shutil.rmtree(caminho)
            
            print(f"\r{Colors.GREEN}✅ Removido com sucesso!{' '*30}{Colors.ENDC}")
            
            with self.lock:
                self.total_removido += 1
                self.total_tamanho += tamanho
                
            return True, tamanho
            
        except Exception as e:
            print(f"\r{Colors.RED}❌ Erro: {str(e)}{' '*30}{Colors.ENDC}")
            with self.lock:
                self.erros.append((caminho, str(e)))
            return False, 0
    
    def processar_paralelo(self, pastas, max_workers=4):
        """Soltando 4 threads pra trabalhar que nem condenado"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}🚀 Iniciando remoção em paralelo ({max_workers} threads)...{Colors.ENDC}\n")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self.remover_pasta, pasta): pasta for pasta in pastas}
            
            for future in as_completed(futures):
                future.result()
    
    def mostrar_resumo(self, tempo_total):
        """Analisando essa bagunça toda pra ver o estrago que fizemos"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.ENDC}")
        print(f"{Colors.CYAN}{Colors.BOLD}📊 RESUMO DA OPERAÇÃO{Colors.ENDC}")
        print(f"{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")
        
        print(f"{Colors.GREEN}✅ Pastas removidas:{Colors.ENDC} {Colors.BOLD}{self.total_removido}{Colors.ENDC}")
        print(f"{Colors.YELLOW}💾 Espaço liberado:{Colors.ENDC} {Colors.BOLD}{self.formatar_tamanho(self.total_tamanho)}{Colors.ENDC}")
        print(f"{Colors.BLUE}⏱️  Tempo total:{Colors.ENDC} {Colors.BOLD}{tempo_total:.2f}s{Colors.ENDC}")
        
        if self.erros:
            print(f"\n{Colors.RED}⚠️  Erros encontrados: {len(self.erros)}{Colors.ENDC}")
            for caminho, erro in self.erros[:5]:  # Mostra apenas os 5 primeiros
                print(f"{Colors.RED}  • {caminho}{Colors.ENDC}")
                print(f"{Colors.RED}    {erro}{Colors.ENDC}")
            if len(self.erros) > 5:
                print(f"{Colors.RED}  ... e mais {len(self.erros) - 5} erros (porque nada é fácil nessa vida){Colors.ENDC}")
        
        print(f"\n{Colors.GREEN}{Colors.BOLD}✨ Operação finalizada!{Colors.ENDC}")
        print(f"{Colors.CYAN}{'='*60}{Colors.ENDC}\n")

def main():
    knife = NodeKnife()
    knife.banner()
    
    # Perguntando onde vocês esconderam essas node_modules
    print(f"{Colors.CYAN}📁 Informe o diretório onde estão seus projetos Node.js:{Colors.ENDC}")
    print(f"{Colors.YELLOW}   (Pressione Enter para usar: C:\\Users\\{os.getlogin()}\\Documents){Colors.ENDC}")
    
    diretorio_input = input(f"{Colors.BOLD}📂 Caminho: {Colors.ENDC}").strip()
    
    # Se não digitou nada, usa o padrão mesmo né
    if not diretorio_input:
        diretorio_alvo = os.path.join("C:\\Users", os.getlogin(), "Documents")
    else:
        diretorio_alvo = diretorio_input
    
    # Verificando se esse caminho existe mesmo ou se vocês inventaram
    if not os.path.exists(diretorio_alvo):
        print(f"{Colors.RED}❌ Diretório não encontrado: {diretorio_alvo}{Colors.ENDC}")
        return
    
    if not os.path.isdir(diretorio_alvo):
        print(f"{Colors.RED}❌ O caminho informado não é um diretório: {diretorio_alvo}{Colors.ENDC}")
        return
    
    print(f"\n{Colors.BOLD}🎯 Diretório alvo:{Colors.ENDC} {diretorio_alvo}\n")
    
    # Última chance de desistir antes da zueira começar
    resposta = input(f"{Colors.YELLOW}⚠️  Deseja continuar? (s/n): {Colors.ENDC}").lower()
    if resposta != 's':
        print(f"{Colors.RED}❌ Operação cancelada.{Colors.ENDC}")
        return
    
    inicio = time.time()
    
    # Começando a caçada a essas node_modules perdidas
    pastas = knife.buscar_node_modules(diretorio_alvo)
    
    if not pastas:
        print(f"\n{Colors.YELLOW}ℹ️  Nenhuma pasta node_modules encontrada.{Colors.ENDC}")
        return
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}🎯 Total encontrado: {len(pastas)} pasta(s){Colors.ENDC}")
    
    # Agora é que a coisa fica séria - hora de deletar tudo
    knife.processar_paralelo(pastas, max_workers=4)
    
    # Vamos ver quantos GBs de lixo a gente conseguiu limpar
    tempo_total = time.time() - inicio
    knife.mostrar_resumo(tempo_total)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}⚠️  Operação interrompida pelo usuário.{Colors.ENDC}")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Erro fatal: {e}{Colors.ENDC}")