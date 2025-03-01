#!/bin/bash

echo "🔍 Verificando se o Docker está instalado..."
if command -v docker &> /dev/null
then
    echo "✅ Docker já está instalado: $(docker --version)"
else
    echo "📌 Instalando Docker..."
    
    sudo apt update && sudo apt upgrade -y
    sudo apt remove docker docker-engine docker.io containerd runc -y
    sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    sudo apt update
    sudo apt install -y docker-ce docker-ce-cli containerd.io

    sudo usermod -aG docker $USER
    echo "⚠️ Reinicie seu sistema ou execute 'newgrp docker' para aplicar as permissões."
fi

echo "🔍 Verificando se o Docker Compose está instalado..."
if command -v docker-compose &> /dev/null
then
    echo "✅ Docker Compose já está instalado: $(docker-compose --version)"
else
    echo "📌 Instalando Docker Compose..."

    latest_version=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep '"tag_name":' | cut -d '"' -f 4)
    sudo curl -L "https://github.com/docker/compose/releases/download/${latest_version}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose

    echo "✅ Docker Compose instalado com sucesso!"
fi

echo "🎉 Instalação finalizada! Verifique com 'docker --version' e 'docker-compose --version'."