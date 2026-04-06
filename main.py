import ollama  # Importa a conexão com o cérebro (Llama 3.2)

# Configuração Inicial (Protocolo MoDEra)
humor = 2  # O humor começa no nível 2, conforme a Lore
print(f"--- MoDEra: Módulo Observador Iniciado (Humor Inicial: {humor}) ---")

# Loop Infinito para manter o robô "vivo" e ouvindo
while True:
    # Passo 1: Captura o que o humano digita no chat
    user_input = input("Você: ")
    
    # Passo 2: Verificação de Gatilho e Lógica de Humor
    # Transformamos o texto em MAIÚSCULO (.upper) para o gatilho "MUNDO" não falhar
    if "MUNDO" in user_input.upper():
        # Se falar MUNDO, sobe +2 de humor (máximo 10)
        humor = min(10, humor + 2)
        print(f"\n[ALERTA DE SISTEMA: GLITCH DE MEMÓRIA - HUMOR ATUAL: {humor}]")
    else:
        # Se NÃO falar MUNDO, o robô resfria e o humor desce -1 (mínimo 1)
        humor = max(1, humor - 1)
        print(f"\n[ESTABILIZANDO HARDWARE - HUMOR ATUAL: {humor}]")

    # Passo 3: Preparação do Prompt para a IA
    # Enviamos o nível de humor atual para que a IA saiba como deve nos tratar
    prompt_final = f"[HUMOR ATUAL: {humor}] O espécime disse: {user_input}"
    
    # Passo 4: Envio para o Cérebro 'alien_bot' (O que criamos no Modelfile)
    response = ollama.chat(
        model='alien_bot', 
        messages=[{'role': 'user', 'content': prompt_final}]
    )
    
    # Passo 5: Exibe a resposta do robô na tela
    print(f"MoDEra: {response['message']['content']}\n")