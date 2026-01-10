# 🌡️ Sistema de Monitoramento Ambiental - Seminário 3

[![Wokwi](https://img.shields.io/badge/Simula%C3%A7%C3%A3o-Wokwi-green)](https://wokwi.com)
[![ESP32](https://img.shields.io/badge/Hardware-ESP32-blue)](https://www.espressif.com/en/products/socs/esp32)
[![MicroPython](https://img.shields.io/badge/Linguagem-MicroPython-yellow)](https://micropython.org/)

## 📌 Sobre o Projeto

Sistema inteligente de monitoramento e controle ambiental desenvolvido para a disciplina de **Sistemas Embarcados** (Janeiro/2026).

**Evolução do Seminário 2:**
- **S2:** Arduino Uno + C/C++ (hardware físico)
- **S3:** ESP32 + MicroPython (simulador Wokwi)

---

## 🎯 Objetivos do Seminário 3

1. ✅ Demonstrar **arquiteturas complementares** (Arduino vs ESP32)
2. ✅ Explorar **linguagens alternativas** (C++ vs MicroPython)
3. ✅ Utilizar **simuladores online** (Wokwi)

---

## 🔧 Componentes de Hardware

### Sensores
| Componente | GPIO | Descrição |
|------------|------|-----------|
| Potenciômetro (LM35) | 34 | Simula sensor de temperatura (0-50°C) |
| Potenciômetro (Setpoint) | 32 | Ajuste do setpoint (20-60°C) |
| LDR (Fotoresistor) | 35 | Sensor de luminosidade |

### Atuadores
| Componente | GPIO | Descrição |
|------------|------|-----------|
| Relé 5V | 25 | Controle de carga (ar-condicionado) |
| Buzzer | 26 | Alarme sonoro (PWM) |
| LED Verde | 27 | Indicador: Normal |
| LED Amarelo | 14 | Indicador: Atenção |
| LED Vermelho | 12 | Indicador: Crítico |

### Controle
| Componente | GPIO | Descrição |
|------------|------|-----------|
| Push Button | 13 | Alternância modo Manual/Automático (PULL_UP) |

---

## 📊 Funcionalidades

### Modo Automático
- Lê temperatura e luminosidade a cada 3 segundos
- Compara temperatura com setpoint ajustável
- **Relé LIGA** quando temperatura > setpoint (refrigeração)
- **Relé DESLIGA** quando temperatura ≤ setpoint

### Indicadores Visuais
| Status | LED | Buzzer | Condição |
|--------|-----|--------|----------|
| 🟢 Normal | Verde | Desligado | temp ≤ setpoint |
| 🟡 Atenção | Amarelo | Desligado | temp > setpoint |
| 🔴 Crítico | Vermelho | Beep | temp > setpoint + 5°C |

### Modo Manual
- Pressionar botão desliga relé e trava (segurança)
- Sistema mantém monitoramento de sensores
- Pressionar novamente retorna ao automático

---

## 📁 Estrutura do Projeto

```
monitoracao_ambiental/
├── README.md
├── LICENSE
├── assets/              # Imagens e recursos
├── docs/                # Documentação
│   ├── relatorio.md
│   ├── apresentacao.md
│   └── referencias.md
└── src/
    └── wokwi/
        ├── diagram.json  # Diagrama do circuito
        └── main.py       # Código MicroPython
```

---

## 🚀 Como Simular no Wokwi

### Opção 1: Importar Manualmente
1. Acesse [Wokwi.com](https://wokwi.com)
2. Crie novo projeto: **New Project → ESP32 → MicroPython**
3. Copie os arquivos de `src/wokwi/`:
   - `diagram.json` → Aba "diagram.json"
   - `main.py` → Aba "main.py"
4. Clique em **Start Simulation ▶️**

### Instruções de Uso
1. 🌡️ **Gire o potenciômetro esquerdo** para simular temperatura (0-50°C)
2. 🎯 **Gire o potenciômetro direito** para ajustar setpoint (20-60°C)
3. 💡 **Clique no LDR** para ajustar luminosidade
4. 🔘 **Pressione o botão azul** para alternar MANUAL/AUTO
5. 👀 **Observe os LEDs**: Verde=OK, Amarelo=Atenção, Vermelho=Crítico

---

## 📖 Documentação

- [Relatório Completo](docs/relatorio.md)
- [Roteiro da Apresentação](docs/apresentacao.md)
- [Referências Bibliográficas](docs/referencias.md)

---


## 📜 Licença

Este projeto está sob a licença MIT - veja [LICENSE](LICENSE) para detalhes.

---

**⭐ Se este projeto foi útil, deixe uma estrela no GitHub!**
