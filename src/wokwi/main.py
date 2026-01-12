# Sistema de Monitoramento Ambiental
# Seminario 3 - Sistemas Embarcados
# ESP32 + MicroPython

from machine import Pin, ADC, PWM
from time import sleep, ticks_ms, ticks_diff
import dht

# Pinos
DHT_PIN = 15
LDR_PIN = 35
POT_PIN = 32
RELAY_PIN = 25
BUTTON_PIN = 13
LED_VERDE_PIN = 27
LED_AMARELO_PIN = 14
LED_VERMELHO_PIN = 12
LED_VENT_PIN = 4
BUZZER_PIN = 26

# Sensores
dht_sensor = dht.DHT22(Pin(DHT_PIN))

light_in = ADC(Pin(LDR_PIN))
light_in.atten(ADC.ATTN_11DB)
light_in.width(ADC.WIDTH_12BIT)

pot_in = ADC(Pin(POT_PIN))
pot_in.atten(ADC.ATTN_11DB)
pot_in.width(ADC.WIDTH_12BIT)

# Atuadores
relay = Pin(RELAY_PIN, Pin.OUT)
relay.off()

button = Pin(BUTTON_PIN, Pin.IN)  # Pull-down externo

led_verde = Pin(LED_VERDE_PIN, Pin.OUT)
led_amarelo = Pin(LED_AMARELO_PIN, Pin.OUT)
led_vermelho = Pin(LED_VERMELHO_PIN, Pin.OUT)
led_verde.off()
led_amarelo.off()
led_vermelho.off()

led_vent = Pin(LED_VENT_PIN, Pin.OUT)
led_vent.off()

buzzer = PWM(Pin(BUZZER_PIN))
buzzer.freq(1000)
buzzer.duty(0)

# Variaveis de estado
temp = 0.0
light_intensity = 0
set_point = 25
previous_millis = 0
INTERVAL = 3000
button_pressed = 0  # 0 = Auto, 1 = Manual
button_last_state = 0
contador = 0


def read_adc_avg(adc_pin, samples=10):
    """Media de leituras ADC para estabilidade."""
    total = 0
    for _ in range(samples):
        total += adc_pin.read()
        sleep(0.001)
    return total // samples


def read_temperature():
    """Le temperatura do DHT22."""
    try:
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        print("  Temp: {:.1f}C | Umidade: {:.1f}%".format(temperature, humidity))
        return temperature
    except:
        return 25.0


def read_temperature_silent():
    """Le temperatura sem print."""
    try:
        dht_sensor.measure()
        return dht_sensor.temperature()
    except:
        return 25.0


def read_light():
    """Le luminosidade do LDR."""
    return read_adc_avg(light_in)


def read_setpoint():
    """Le setpoint do potenciometro (20-60C)."""
    adc_value = read_adc_avg(pot_in)
    return int(20 + (adc_value / 4095.0) * 40)


def update_leds(temperature, setpoint):
    """Atualiza LEDs conforme temperatura."""
    diff = temperature - setpoint
    
    led_verde.off()
    led_amarelo.off()
    led_vermelho.off()
    buzzer.duty(0)
    
    if diff > 5:
        led_vermelho.on()
        buzzer.duty(512)
        sleep(0.1)
        buzzer.duty(0)
        return "CRITICO"
    elif diff > 0:
        led_amarelo.on()
        return "ATENCAO"
    else:
        led_verde.on()
        return "NORMAL"


def control_relay(temperature, setpoint, manual_mode):
    """Controla rele automaticamente ou manual."""
    if manual_mode:
        if relay.value():
            relay.off()
            led_vent.off()
            print("Rele DESLIGADO - Modo Manual")
    else:
        if temperature > setpoint:
            if not relay.value():
                relay.on()
                led_vent.on()
                print("Rele LIGADO - Temp {:.1f}C > Setpoint {}C".format(temperature, setpoint))
        else:
            if relay.value():
                relay.off()
                led_vent.off()
                print("Rele DESLIGADO - Temp {:.1f}C <= Setpoint {}C".format(temperature, setpoint))


def display_data(temp_c, light, setpoint, status, relay_on, manual_mode, reading_num):
    """Exibe dados no terminal."""
    temp_f = temp_c * 1.8 + 32
    modo = "MANUAL" if manual_mode else "AUTO"
    rele = "LIGADO" if relay_on else "DESLIGADO"
    
    print("\n--- Leitura #{} ---".format(reading_num))
    print("Temperatura: {:.1f}C / {:.1f}F".format(temp_c, temp_f))
    print("Luminosidade: {}".format(light))
    print("Setpoint: {}C".format(setpoint))
    print("Status: {}".format(status))
    print("Rele: {} | Modo: {}".format(rele, modo))
    print("------------------\n")


# Mensagem inicial
print("\n=== Sistema de Monitoramento Ambiental ===")
print("Iniciando...\n")
sleep(2)

# Loop principal
try:
    while True:
        current_millis = ticks_ms()
        
        # Leitura periodica (a cada 3 segundos)
        if ticks_diff(current_millis, previous_millis) >= INTERVAL:
            previous_millis = current_millis
            contador += 1
            
            temp = read_temperature()
            light_intensity = read_light()
            set_point = read_setpoint()
            
            status = update_leds(temp, set_point)
            
            display_data(temp, light_intensity, set_point, status, 
                        relay.value(), button_pressed, contador)
        
        # Leitura continua para controle do rele
        temp = read_temperature_silent()
        set_point = read_setpoint()
        control_relay(temp, set_point, button_pressed)
        
        # Deteccao do botao
        button_current = button.value()
        
        if button_current == 1 and button_last_state == 0:
            if button_pressed == 0:
                button_pressed = 1
                relay.off()
                print("\n>> MODO MANUAL ATIVADO <<\n")
            else:
                button_pressed = 0
                print("\n>> MODO AUTOMATICO ATIVADO <<\n")
            sleep(0.3)
        
        button_last_state = button_current
        sleep(0.05)

except KeyboardInterrupt:
    relay.off()
    led_verde.off()
    led_amarelo.off()
    led_vermelho.off()
    led_vent.off()
    buzzer.duty(0)
    print("\nSistema finalizado. {} leituras realizadas.".format(contador))
