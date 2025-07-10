#!/bin/bash

# Script para corrigir dependências do Tribo do Cerrado
# Execute este arquivo para fazer tudo automaticamente

echo "🚀 Iniciando correção de dependências do Tribo do Cerrado..."

# Passo 1: Backup
echo "📦 Fazendo backup..."
git checkout -b backup-correcao-$(date +%Y%m%d-%H%M%S)
git push origin backup-correcao-$(date +%Y%m%d-%H%M%S)
git checkout main

# Passo 2: Remover dependências problemáticas
echo "🗑️ Removendo versões problemáticas..."
npm uninstall react-day-picker date-fns

# Passo 3: Instalar versão correta
echo "⬇️ Instalando react-day-picker 9.x..."
npm install react-day-picker@^9.8.0

# Passo 4: Limpar cache
echo "🧹 Limpando cache..."
rm -rf node_modules package-lock.json
npm install

# Passo 5: Testar build
echo "🔨 Testando build..."
if npm run build; then
    echo "✅ Build funcionou! Sucesso!"
    
    # Passo 6: Commit das mudanças
    echo "💾 Salvando mudanças..."
    git add .
    git commit -m "fix: atualizar react-day-picker para v9.x - resolve conflito de dependências"
    git push origin main
    
    echo "🎉 Correção concluída com sucesso!"
    echo "Seu projeto agora deve funcionar no Vercel!"
else
    echo "❌ Build falhou. Tentando solução alternativa..."
    npm install --legacy-peer-deps
    
    if npm run build; then
        echo "✅ Build funcionou com legacy-peer-deps!"
        git add .
        git commit -m "fix: resolver conflito de dependências com legacy-peer-deps"
        git push origin main
    else
        echo "❌ Ainda há problemas. Restaurando backup..."
        git checkout backup-correcao-$(date +%Y%m%d-%H%M%S)
        npm install
        echo "🔄 Projeto restaurado ao estado anterior"
    fi
fi

