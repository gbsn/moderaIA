import os, datetime, vosk, pyaudio, json, ollama, gc
from murf import Murf, MurfRegion

# =============================================================================
# 1. SISTEMA DE LOGS COM ID CRESCENTE E DATA/HORA
# =============================================================================
LOG_FOLDER = "logs"
if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER) # Garante que a pasta de registros exista

def obter_proximo_id():
    """Varre a pasta de logs para encontrar o maior ID e somar +1"""
    arquivos = [f for f in os.listdir(LOG_FOLDER) if f.endswith(".txt")]
    ids = []
    for f in arquivos:
        try:
            # Tenta pegar o primeiro número do nome do arquivo (o ID)
            primeira_parte = f.split(' ')[0]
            ids.append(int(primeira_parte))
        except (ValueError, IndexError):
            continue
    return max(ids) + 1 if ids else 1

# Configuração do nome do arquivo: ID DDMMYYYY HHMM
novo_id = obter_proximo_id()
data_formatada = datetime.datetime.now().strftime("%d%m%Y")
hora_formatada = datetime.datetime.now().strftime("%H%M")
log_path = os.path.join(LOG_FOLDER, f"{novo_id} {data_formatada} {hora_formatada}.txt")

def gravar_log(quem, mensagem, humor_atual):
    """Escreve a interação no arquivo de texto com carimbo de tempo"""
    hora_fala = datetime.datetime.now().strftime("%H:%M:%S")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{hora_fala}] | HUMOR: {humor_atual} | {quem}: {mensagem}\n")

# =============================================================================
# 2. CONFIGURAÇÕES DE HARDWARE (OUVIDOS E VOZ)
# =============================================================================
# [ALERTA DE PRIVACIDADE]: Oculte a tela antes de inserir sua chave!
MURFA_API_KEY = "ap2_1124bfa0-7e38-4ef0-8e18-7cb0c292274e"
murf_client = Murf(api_key=MURFA_API_KEY, region=MurfRegion.GLOBAL)

# Inicializa o motor de reconhecimento de voz (Offline)
model = vosk.Model("model")
rec = vosk.KaldiRecognizer(model, 16000)

# Inicializa o motor de áudio (PyAudio)
p = pyaudio.PyAudio()
# Canal de Entrada (Microfone - 16kHz)
stream_in = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
# Canal de Saída (Caixas de Som - 24kHz para alta fidelidade do Murf)
stream_out = p.open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)
stream_in.start_stream()

# =============================================================================
# 3. ESTADO MENTAL E LORE DO MoDEra
# =============================================================================
humor = 2
primeira_vez = True

print(f"--- MoDEra: Módulo de Observação Ativo (Log #{novo_id}) ---")
gravar_log("SISTEMA", "Sessão iniciada e hardware conectado.", humor)

# =============================================================================
# 4. LOOP PRINCIPAL DE INTERAÇÃO
# =============================================================================
try:
    while True:
        # Escuta o ambiente continuamente
        data = stream_in.read(4000, exception_on_overflow=False)
        
        if rec.AcceptWaveform(data):
            resultado = json.loads(rec.Result())
            user_input = resultado['text'].upper() # Gatilhos em maiúsculo
            
            if user_input.strip():
                print(f"\nEspécime: {user_input}")
                gravar_log("HUMANO", user_input, humor)

                # --- PROTOCOLO DE DESLIGAMENTO E FLUSH DE MEMÓRIA ---
                if "MODERA DESLIGA" in user_input:
                    print("\nMoDEra: Estase iniciada. Realizando Flush de dados...")
                    gravar_log("SISTEMA", "Protocolo de desligamento executado.", humor)
                    # Liberação de Hardware
                    stream_in.stop_stream(); stream_in.close()
                    stream_out.stop_stream(); stream_out.close()
                    p.terminate()
                    # Limpeza de Memória RAM (Garbage Collector)
                    gc.collect()
                    break

                # --- LÓGICA DE PERSONALIDADE E HUMOR ---
                if primeira_vez:
                    prompt = f"[INICIALIZAÇÃO] {user_input}"
                    primeira_vez = False
                elif "MUNDO" in user_input:
                    humor = min(10, humor + 2) # Gatilho 'MUNDO' irrita o robô
                    prompt = f"[GLITCH DIMENSIONAL - HUMOR {humor}] {user_input}"
                else:
                    humor = max(1, humor - 1) # Resfriamento térmico (IA se acalma)
                    prompt = f"[HUMOR ATUAL {humor}] {user_input}"

                # --- PROCESSAMENTO NO OLLAMA ---
                response = ollama.chat(model='alien_bot', messages=[{'role': 'user', 'content': prompt}])
                texto_resposta = response['message']['content']
                
                print(f"MoDEra: {texto_resposta}\n")
                gravar_log("MoDEra", texto_resposta, humor)

                # --- GERAÇÃO E STREAMING DE VOZ (MURF) ---
                audio_stream = murf_client.text_to_speech.stream(
                    text=texto_resposta, 
                    voice_id="Heitor", # Exemplo de voz brasileira, mude se desejar
                    model="FALCON",
                    format="PCM",
                    sample_rate=24000

                )
                # Toca o áudio em tempo real enquanto o Murf gera o som
                for chunk in audio_stream:
                    if chunk: stream_out.write(chunk)

                print("[SENSORES EM ALERTA]")

except KeyboardInterrupt:
    # Caso você aperte Ctrl+C no terminal
    p.terminate()
    print("\nInterrupção manual detectada. Sistemas desligados.")



#---> Segunda versão Modera
'''
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

#--->Primeira versão Modera
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