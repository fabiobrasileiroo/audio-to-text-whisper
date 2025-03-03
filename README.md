OpenAI Whisper - Transcrição de Áudio com Docker 🚀

Este projeto usa o OpenAI Whisper para transcrição de áudio de forma local, com suporte a Docker para facilitar a instalação e execução.

📌 Como Executar

🔹 Instalar o Docker

Se ainda não possui o Docker instalado, utilize o script fornecido:

Linux:
``` bash 
chmod +x install_docker_linux.sh ./install_docker_linux.sh
``` 

Windows (PowerShell como Administrador):
``` powershell
Set-ExecutionPolicy Unrestricted -Scope Process ./install_docker_windows.ps1
``` 

🔹 Executar o Projeto

Após instalar o Docker, basta rodar:

``` bash 
docker-compose up --build
```
### Exemplo de uso no postman, mas podemos usar com curl também:
![%Y-%m%d_](https://github.com/user-attachments/assets/55b465c9-45d7-41b2-b4ce-b4a9637cebf3)



O serviço estará rodando e pronto para receber áudios para transcrição!


