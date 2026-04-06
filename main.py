import vosk, pyaudio, json, ollama

# 1. Configurações de Áudio e Carregamento do Modelo
model = vosk.Model("model")
rec = vosk.KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

# 2. Variáveis de Estado do MoDEra
humor = 2
primeira_vez = True

print("--- MoDEra: Módulo de Observação Ativo ---")
print("[SISTEMA EM ALERTA - AGUARDANDO INTERAÇÃO...]")

# 3. Loop Principal de Audição e Resposta
while True:
    data = stream.read(4000, exception_on_overflow=False)
    
    if rec.AcceptWaveform(data):
        resultado = json.loads(rec.Result())
        user_input = resultado['text'].upper()
        
        if user_input.strip(): # Verifica se o humano realmente falou algo
            print(f"\nEspécime: {user_input}")

            # --- NOVO: PROTOCOLO DE DESLIGAMENTO ---
            if "MODERA DESLIGA" in user_input:
                print("\nMoDEra: Protocolo de estase iniciado. Conexão dimensional encerrada.")
                stream.stop_stream()
                stream.close()
                p.terminate()
                break 

            # 4. Lógica de Humor e Gatilho "MUNDO"
            if primeira_vez:
                prompt = f"[INICIALIZAÇÃO] {user_input}"
                primeira_vez = False
            elif "MUNDO" in user_input:
                humor = min(10, humor + 2)
                prompt = f"[GLITCH - HUMOR {humor}] {user_input}"
            else:
                humor = max(1, humor - 1)
                prompt = f"[HUMOR {humor}] {user_input}"

            # 5. Envio dos dados para o Cérebro (Ollama)
            response = ollama.chat(model='alien_bot', messages=[{'role': 'user', 'content': prompt}])
            print(f"MoDEra: {response['message']['content']}\n")
            
            # 6. Feedback de Escuta
            status = "[SISTEMA EM ALERTA - AGUARDANDO INTERAÇÃO]" if humor < 8 else "[SISTEMA SOBRECARREGADO - DIGA ALGO LOGO!]"
            print(f"{status}")



'''
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
    '''