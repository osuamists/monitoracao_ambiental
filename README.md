# Sistema de Monitoramento Ambiental - Seminário 3

[![Wokwi](https://img.shields.io/badge/Simulação-Wokwi-green)](https://wokwi.com)
[![ESP32](https://img.shields.io/badge/Hardware-ESP32-blue)](https://www.espressif.com/en/products/socs/esp32)
[![MicroPython](https://img.shields.io/badge/Linguagem-MicroPython-yellow)](https://micropython.org/)

## Sobre o Projeto

Sistema de monitoramento e controle ambiental desenvolvido para a disciplina de **Sistemas Embarcados**.

**Evolução do Seminário 2:**
- **S2:** Arduino Uno + C/C++ (hardware físico)
- **S3:** ESP32 + MicroPython (simulador Wokwi)

---

## Objetivos

1. Demonstrar arquiteturas complementares (Arduino vs ESP32)
2. Explorar linguagens alternativas (C++ vs MicroPython)
3. Utilizar simuladores online (Wokwi)

---

## Componentes de Hardware

### Sensores
| Componente | GPIO | Descrição |
|------------|------|-----------|
| DHT22 | 15 | Sensor de temperatura e umidade |
| Potenciômetro | 32 | Ajuste do setpoint (20-60°C) |
| LDR | 35 | Sensor de luminosidade |

### Atuadores
| Componente | GPIO | Descrição |
|------------|------|-----------|
| Relé 5V | 25 | Controle de ventilação |
| Buzzer | 26 | Alarme sonoro (PWM) |
| LED Verde | 27 | Indicador: Normal |
| LED Amarelo | 14 | Indicador: Atenção |
| LED Vermelho | 12 | Indicador: Crítico |
| LED Azul | - | Indicador de ventilação (via relé NO) |

### Controle
| Componente | GPIO | Descrição |
|------------|------|-----------|
| Push Button | 13 | Alternância Manual/Automático (pull-down externo 10kΩ) |

---

## Funcionalidades

### Modo Automático
- Lê temperatura e umidade do DHT22 a cada 3 segundos
- Compara temperatura com setpoint ajustável
- **Relé LIGA** quando temperatura > setpoint (ventilação)
- **Relé DESLIGA** quando temperatura ≤ setpoint
- LED azul indica quando ventilação está ativa

### Indicadores Visuais
| Status | LED | Buzzer | Condição |
|--------|-----|--------|----------|
| Normal | Verde | Desligado | temp ≤ setpoint |
| Atenção | Amarelo | Desligado | temp > setpoint |
| Crítico | Vermelho | Beep | temp > setpoint + 5°C |

### Modo Manual
- Pressionar botão desliga relé e trava
- Sistema mantém monitoramento de sensores
- Pressionar novamente retorna ao automático

---

## Estrutura do Projeto

```
monitoracao_ambiental/
├── README.md
├── LICENSE
├── assets/
├── docs/
└── src/
    └── wokwi/
        ├── diagram.json  # Circuito Wokwi
        └── main.py       # Código MicroPython
```

---

## Como Simular no Wokwi

1. Acesse [Wokwi.com](https://wokwi.com)
2. Crie novo projeto: **New Project → ESP32 → MicroPython**
3. Copie os arquivos de `src/wokwi/`:
   - `diagram.json` → Aba "diagram.json"
   - `main.py` → Aba "main.py"
4. Clique em **Start Simulation**

### Instruções de Uso
1. O DHT22 tem temperatura inicial de 24°C (clique para ajustar)
2. Gire o potenciômetro para ajustar setpoint (20-60°C)
3. Clique no LDR para ajustar luminosidade
4. Pressione o botão para alternar MANUAL/AUTO
5. Observe os LEDs e o LED azul (ventilação)

---

## Licença

Este projeto está sob a licença MIT - veja [LICENSE](LICENSE) para detalhes.
