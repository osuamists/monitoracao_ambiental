# ==============================================================
# SEMINÁRIO 3 - Sistema de Monitoramento Ambiental
# Disciplina: Sistemas Embarcados
# Migração: Arduino Uno C++ (S2) → ESP32 MicroPython (S3)
# ==============================================================
# Autor: Equipe de Monitoramento Ambiental
# Data: Janeiro/2026
# Versão: 2.0 - Versão Final Funcional
# ==============================================================

# ==============================================================
# 1. IMPORTS
# ==============================================================
from machine import Pin, ADC, PWM
from time import sleep, ticks_ms, ticks_diff

# ==============================================================
# 2. BANNER E IDENTIFICAÇÃO
# ==============================================================
print("\n" + "="*75)
print("  🌡️  SISTEMA DE MONITORAMENTO AMBIENTAL - SEMINÁRIO 3")
print("  📌 Arduino Uno C++ (S2) → ESP32 MicroPython (S3)")
print("  🎓 Disciplina: Sistemas Embarcados")
print("="*75 + "\n")

# ==============================================================
# 3. CONFIGURAÇÃO DE HARDWARE
# ==============================================================

print("🔧 CONFIGURANDO HARDWARE...")
print("-" * 40)

# --------------------------------------------------------------
# 3.1 Sensores Analógicos (ADC)
# --------------------------------------------------------------

# LM35 - Sensor de Temperatura (GPIO34 - ADC1_CH6)
# No Wokwi: Potenciômetro simula o sensor
LM35_PIN = 34
temp_in = ADC(Pin(LM35_PIN))
temp_in.atten(ADC.ATTN_11DB)    # Range: 0-3.3V
temp_in.width(ADC.WIDTH_12BIT)  # Resolução: 12 bits (0-4095)
print("   ✅ LM35 - Sensor Temperatura (GPIO{})".format(LM35_PIN))

# LDR - Sensor de Luminosidade (GPIO35 - ADC1_CH7)
LDR_PIN = 35
light_in = ADC(Pin(LDR_PIN))
light_in.atten(ADC.ATTN_11DB)
light_in.width(ADC.WIDTH_12BIT)
print("   ✅ LDR - Sensor Luminosidade (GPIO{})".format(LDR_PIN))

# Potenciômetro - Ajuste de Setpoint (GPIO32 - ADC1_CH4)
POT_PIN = 32
pot_in = ADC(Pin(POT_PIN))
pot_in.atten(ADC.ATTN_11DB)
pot_in.width(ADC.WIDTH_12BIT)
print("   ✅ Potenciômetro - Setpoint (GPIO{})".format(POT_PIN))

# --------------------------------------------------------------
# 3.2 Atuadores Digitais
# --------------------------------------------------------------

# Relé - Controle de Carga (GPIO25)
RELAY_PIN = 25
relay = Pin(RELAY_PIN, Pin.OUT)
relay.off()
print("   ✅ Relé - Controle de Carga (GPIO{})".format(RELAY_PIN))

# Botão - Modo Manual/Automático (GPIO13 com PULL_UP)
BUTTON_PIN = 13
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)
print("   ✅ Botão - Manual/Auto (GPIO{}) - PULL_UP".format(BUTTON_PIN))

# --------------------------------------------------------------
# 3.3 LEDs Indicadores
# --------------------------------------------------------------

LED_VERDE_PIN = 27    # Normal
LED_AMARELO_PIN = 14  # Atenção
LED_VERMELHO_PIN = 12 # Crítico

led_verde = Pin(LED_VERDE_PIN, Pin.OUT)
led_amarelo = Pin(LED_AMARELO_PIN, Pin.OUT)
led_vermelho = Pin(LED_VERMELHO_PIN, Pin.OUT)

# Inicializa LEDs desligados
led_verde.off()
led_amarelo.off()
led_vermelho.off()
print("   ✅ LED Verde - Normal (GPIO{})".format(LED_VERDE_PIN))
print("   ✅ LED Amarelo - Atenção (GPIO{})".format(LED_AMARELO_PIN))
print("   ✅ LED Vermelho - Crítico (GPIO{})".format(LED_VERMELHO_PIN))

# --------------------------------------------------------------
# 3.4 Buzzer (PWM)
# --------------------------------------------------------------

BUZZER_PIN = 26
buzzer = PWM(Pin(BUZZER_PIN))
buzzer.freq(1000)  # Frequência: 1kHz
buzzer.duty(0)     # Inicia desligado
print("   ✅ Buzzer - Alarme Sonoro (GPIO{})".format(BUZZER_PIN))

print("-" * 40)
print("✅ HARDWARE INICIALIZADO COM SUCESSO!\n")

# ==============================================================
# 4. VARIÁVEIS GLOBAIS
# ==============================================================

# Valores dos sensores
temp = 0.0
light_intensity = 0
set_point = 25

# Controle de tempo (temporização não-bloqueante)
previous_millis = 0
INTERVAL = 3000  # 3 segundos entre leituras

# Controle do botão
button_pressed = 0      # 0 = Automático, 1 = Manual
button_last_state = 1   # PULL_UP: estado inicial = 1 (HIGH)

# Contador de leituras
contador = 0

# ==============================================================
# 5. FUNÇÕES DE LEITURA
# ==============================================================

def read_adc_avg(adc_pin, samples=10):
    """
    Lê ADC com média de múltiplas amostras para estabilizar leitura.
    Reduz ruído e flutuações do ADC do ESP32.
    
    Args:
        adc_pin: Objeto ADC configurado
        samples: Número de amostras para média (default: 10)
    
    Returns:
        int: Valor médio do ADC (0-4095)
    """
    total = 0
    for _ in range(samples):
        total += adc_pin.read()
        sleep(0.001)  # 1ms entre leituras
    return total // samples


def read_temperature():
    """
    Lê o sensor LM35 e retorna temperatura em °C.
    
    WOKWI: Como não existe LM35 real, usamos potenciômetro
           mapeado para range 0-50°C para simulação.
    
    HARDWARE REAL: temp = (adc_value / 4095.0) * 3.3 * 100
                   LM35 fornece 10mV/°C
    
    Returns:
        float: Temperatura em graus Celsius
    """
    adc_value = read_adc_avg(temp_in)
    
    # WOKWI: Mapeia potenciômetro para 0-50°C
    temperature = (adc_value / 4095.0) * 50.0
    
    # Debug detalhado
    print("   [DEBUG] ADC LM35: {:4d} | Temp: {:.2f}°C".format(
        adc_value, temperature))
    
    return temperature


def read_temperature_silent():
    """
    Lê temperatura sem mensagens de debug.
    Usado para leitura contínua no loop principal.
    
    Returns:
        float: Temperatura em graus Celsius
    """
    adc_value = read_adc_avg(temp_in)
    return (adc_value / 4095.0) * 50.0


def read_light_intensity():
    """
    Lê o sensor LDR e retorna valor de luminosidade.
    
    Returns:
        int: Valor ADC da luminosidade (0-4095)
             0 = Escuro, 4095 = Muito claro
    """
    adc_value = read_adc_avg(light_in)
    print("   [DEBUG] ADC LDR: {:4d}".format(adc_value))
    return adc_value


def read_setpoint():
    """
    Lê o potenciômetro e retorna o setpoint de temperatura.
    Range configurável: 20°C a 60°C
    
    Returns:
        int: Setpoint em graus Celsius (20-60)
    """
    adc_value = read_adc_avg(pot_in)
    
    # Mapeia ADC (0-4095) para temperatura (20-60°C)
    setpoint = int(20 + (adc_value / 4095.0) * 40)
    
    print("   [DEBUG] ADC POT: {:4d} | Setpoint: {}°C".format(
        adc_value, setpoint))
    
    return setpoint


def read_setpoint_silent():
    """
    Lê setpoint sem mensagens de debug.
    Usado para leitura contínua no loop principal.
    
    Returns:
        int: Setpoint em graus Celsius (20-60)
    """
    adc_value = read_adc_avg(pot_in)
    return int(20 + (adc_value / 4095.0) * 40)


# ==============================================================
# 6. FUNÇÕES DE CONTROLE
# ==============================================================

def update_leds(temperature, setpoint):
    """
    Atualiza LEDs indicadores e buzzer baseado na temperatura.
    
    Lógica:
    - LED Verde:    temp <= setpoint         → NORMAL
    - LED Amarelo:  temp > setpoint          → ATENÇÃO
    - LED Vermelho: temp > setpoint + 5°C    → CRÍTICO (+ buzzer)
    
    Args:
        temperature: Temperatura atual em °C
        setpoint: Temperatura de referência em °C
    
    Returns:
        str: Status do sistema com emoji
    """
    diff = temperature - setpoint
    
    # Desliga todos primeiro
    led_verde.off()
    led_amarelo.off()
    led_vermelho.off()
    buzzer.duty(0)
    
    # Avalia condição
    if diff > 5:
        # CRÍTICO: Temperatura muito alta
        led_vermelho.on()
        # Beep curto de alarme
        buzzer.duty(512)
        sleep(0.1)
        buzzer.duty(0)
        return "🔴 CRÍTICO"
        
    elif diff > 0:
        # ATENÇÃO: Temperatura acima do setpoint
        led_amarelo.on()
        return "🟡 ATENÇÃO"
        
    else:
        # NORMAL: Temperatura OK
        led_verde.on()
        return "🟢 NORMAL"


def control_relay(temperature, setpoint, manual_mode):
    """
    Controla o relé baseado na temperatura e modo de operação.
    
    Modo Automático:
    - Liga relé quando temp > setpoint
    - Desliga relé quando temp <= setpoint
    
    Modo Manual:
    - Relé permanece desligado
    
    Args:
        temperature: Temperatura atual em °C
        setpoint: Temperatura de referência em °C
        manual_mode: 0 = Automático, 1 = Manual
    """
    if manual_mode:
        # Modo Manual: relé sempre desligado
        if relay.value():
            relay.off()
            print("\n🔌 RELÉ DESLIGADO - Modo Manual")
    else:
        # Modo Automático
        if temperature > setpoint:
            if not relay.value():
                relay.on()
                print("\n🔌 RELÉ LIGADO - Temp {:.1f}°C > Setpoint {}°C".format(
                    temperature, setpoint))
        else:
            if relay.value():
                relay.off()
                print("\n🔌 RELÉ DESLIGADO - Temp {:.1f}°C <= Setpoint {}°C".format(
                    temperature, setpoint))


def display_data(temp_c, temp_f, light, setpoint, status, relay_on, manual_mode, reading_num):
    """
    Exibe dados formatados no Serial Monitor.
    Inclui simulação visual do LCD 16x2.
    
    Args:
        temp_c: Temperatura em Celsius
        temp_f: Temperatura em Fahrenheit
        light: Valor de luminosidade
        setpoint: Setpoint atual
        status: String de status
        relay_on: Estado do relé
        manual_mode: Modo de operação
        reading_num: Número da leitura
    """
    print("\n" + "="*75)
    print("📊 DADOS DO SISTEMA - Leitura #{}".format(reading_num))
    print("="*75)
    print("🌡️  Temperatura: {:.2f}°C | {:.2f}°F".format(temp_c, temp_f))
    print("💡 Luminosidade: {} (ADC)".format(light))
    print("🎯 Setpoint: {}°C".format(setpoint))
    print("🚦 Status: {}".format(status))
    print("🔌 Relé: {}".format("⚡ LIGADO" if relay_on else "○ DESLIGADO"))
    print("🎮 Modo: {}".format("🔧 MANUAL" if manual_mode else "🤖 AUTOMÁTICO"))
    print("="*75)
    
    # Simulação visual do LCD 16x2
    modo_txt = "MAN" if manual_mode else "AUTO"
    print("\n📺 DISPLAY LCD 16x2:")
    print("┌────────────────────┐")
    print("│ T:{:5.1f}C SP:{:2d}C   │".format(temp_c, setpoint))
    print("│ Luz:{:4d}  {:4s}   │".format(light, modo_txt))
    print("└────────────────────┘\n")


# ==============================================================
# 7. SETUP INICIAL
# ==============================================================

print("📊 Configuração Inicial:")
print("   - Setpoint padrão: {}°C".format(set_point))
print("   - Intervalo de leitura: {} segundos".format(INTERVAL/1000))
print("   - Modo inicial: AUTOMÁTICO")
print("   - Range Setpoint: 20-60°C")
print("   - Range Temperatura (Wokwi): 0-50°C\n")

print("="*75)
print("  📖 INSTRUÇÕES DE USO:")
print("="*75)
print("  1. 🌡️  Gire o potenciômetro 'LM35' para simular temperatura")
print("  2. 🎯 Gire o potenciômetro 'Setpoint' para ajustar referência")
print("  3. 💡 Clique no LDR para ajustar luminosidade")
print("  4. 🔘 Pressione o botão azul para alternar MANUAL/AUTO")
print("  5. 👀 Observe os LEDs: Verde=OK, Amarelo=Atenção, Vermelho=Crítico")
print("="*75 + "\n")

# Aguarda 2 segundos antes de iniciar
print("⏳ Iniciando em 2 segundos...")
sleep(2)

# ==============================================================
# 8. LOOP PRINCIPAL
# ==============================================================

print("\n" + "🔄"*37)
print("        🚀 INICIANDO MONITORAMENTO AMBIENTAL 🚀")
print("🔄"*37 + "\n")

try:
    while True:
        # Obtém tempo atual
        current_millis = ticks_ms()
        
        # --------------------------------------------------------
        # 8.1 Leitura e Exibição Periódica (a cada 3 segundos)
        # --------------------------------------------------------
        if ticks_diff(current_millis, previous_millis) >= INTERVAL:
            previous_millis = current_millis
            contador += 1
            
            # Cabeçalho da leitura
            print("\n" + "-"*75)
            print("📡 LEITURA #{} - Tempo: {}ms".format(contador, current_millis))
            print("-"*75)
            
            # Lê todos os sensores (com debug)
            temp = read_temperature()
            light_intensity = read_light_intensity()
            set_point = read_setpoint()
            
            # Converte para Fahrenheit
            temp_f = temp * (9.0 / 5.0) + 32.0
            
            # Atualiza LEDs e obtém status
            status = update_leds(temp, set_point)
            
            # Exibe dados formatados
            display_data(
                temp, temp_f, light_intensity, set_point,
                status, relay.value(), button_pressed, contador
            )
        
        # --------------------------------------------------------
        # 8.2 Leitura Contínua Silenciosa (para controle do relé)
        # --------------------------------------------------------
        temp = read_temperature_silent()
        set_point = read_setpoint_silent()
        
        # --------------------------------------------------------
        # 8.3 Controle do Relé
        # --------------------------------------------------------
        control_relay(temp, set_point, button_pressed)
        
        # --------------------------------------------------------
        # 8.4 Detecção do Botão (com debounce)
        # PULL_UP: Solto = 1 (HIGH), Pressionado = 0 (LOW)
        # --------------------------------------------------------
        button_current_state = button.value()
        
        # Detecta borda de descida (1 -> 0) = botão pressionado
        if button_current_state == 0 and button_last_state == 1:
            # Alterna modo
            if button_pressed == 0:
                button_pressed = 1
                relay.off()
                print("\n" + "🔴"*25)
                print("  >>> BOTÃO PRESSIONADO <<<")
                print("  >>> MODO MANUAL ATIVADO <<<")
                print("  >>> Relé desligado e travado <<<")
                print("🔴"*25 + "\n")
            else:
                button_pressed = 0
                print("\n" + "🟢"*25)
                print("  >>> BOTÃO PRESSIONADO <<<")
                print("  >>> MODO AUTOMÁTICO ATIVADO <<<")
                print("  >>> Controle automático do relé <<<")
                print("🟢"*25 + "\n")
            
            # Debounce: aguarda 300ms
            sleep(0.3)
        
        # Atualiza estado anterior do botão
        button_last_state = button_current_state
        
        # --------------------------------------------------------
        # 8.5 Delay do Loop
        # --------------------------------------------------------
        sleep(0.05)  # 50ms - evita sobrecarga do processador

# ==============================================================
# 9. TRATAMENTO DE INTERRUPÇÃO
# ==============================================================
except KeyboardInterrupt:
    print("\n\n" + "⚠️"*25)
    print("     SISTEMA INTERROMPIDO PELO USUÁRIO")
    print("⚠️"*25)
    
    # Desliga todos os atuadores
    relay.off()
    led_verde.off()
    led_amarelo.off()
    led_vermelho.off()
    buzzer.duty(0)
    
    print("\n✅ Todos os atuadores foram desligados com segurança")
    print("📊 Total de leituras realizadas: {}".format(contador))
    print("👋 Sistema finalizado.\n")

# ==============================================================
# FIM DO CÓDIGO
# ==============================================================
