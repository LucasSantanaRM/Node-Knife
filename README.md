# 🔪 Node Knife - Limpador de node_modules

> *"Porque ninguém merece ter 50GB de node_modules ocupando o HD"*

## O que é essa bagaça?

Cara, se você é dev e trabalha com Node.js, você já sabe o drama: essas pastas `node_modules` ficam espalhadas por todo canto do seu PC, ocupando um espaço absurdo. Esse script aqui é pra resolver essa bagunça de uma vez por todas!

O **Node Knife** é um limpador turbinado que:
- 🔍 Vasculha seu PC inteiro procurando essas node_modules perdidas
- 📊 Mostra quanto espaço cada uma tá ocupando (pra você chorar)
- 🚀 Deleta tudo em paralelo (4 threads trabalhando que nem condenado)
- 🎨 Faz isso tudo com uma interface coloridinha e bonitinha

## Como usar essa maravilha?

### 1. Primeiro, instala as dependências:
```bash
pip install -r requirements.txt
```

### 2. Roda o script:
```bash
python app.py
```

### 3. Segue o roteiro:
- O script vai perguntar onde estão seus projetos
- Se não souber, só aperta Enter que ele usa a pasta Documents
- Confirma se quer continuar (última chance de desistir!)
- Senta e relaxa enquanto ele faz a faxina

## Exemplo de uso:

```
📁 Informe o diretório onde estão seus projetos Node.js:
   (Pressione Enter para usar: C:\Users\Lucas\Documents)
📂 Caminho: C:\dev\projetos

🎯 Diretório alvo: C:\dev\projetos

⚠️  Deseja continuar? (s/n): s

⏳ Escaneando diretórios...
📂 Base: C:\dev\projetos

✓ Encontrado: C:\dev\projetos\meu-app\node_modules
✓ Encontrado: C:\dev\projetos\outro-projeto\node_modules

🎯 Total encontrado: 2 pasta(s)

🚀 Iniciando remoção em paralelo (4 threads)...

============================================================
📊 RESUMO DA OPERAÇÃO
============================================================

✅ Pastas removidas: 2
💾 Espaço liberado: 1.2 GB
⏱️  Tempo total: 45.32s

✨ Operação finalizada!
```

## ⚠️ Avisos importantes:

- **NÃO** deleta seus arquivos de código (package.json, src/, etc.)
- **SÓ** remove as pastas `node_modules`
- Depois de rodar, é só fazer `npm install` nos projetos pra baixar tudo de novo
- Testado no Windows (se você usa Linux, se vira aí)

## Por que fiz isso?

Porque cansei de ver meu SSD chorando com 30GB de `node_modules` espalhadas. Agora toda semana eu rodo esse script e libero uns bons GBs de espaço.

## Contribuições

Achou algum bug? Quer melhorar alguma coisa? Manda um PR aí que eu analiso!

---

**Feito com ☕ e muito ódio pelas node_modules**
