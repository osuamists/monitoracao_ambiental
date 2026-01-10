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
- **LM35:** Sensor de temperatura (-55°C a 150°C)
- **LDR:** Fotoresistor (luminosidade)
- **Potenciômetro:** Ajuste de setpoint (20-60°C)

### Atuadores
- **Relé 5V:** Controle de carga (simulação de ar-condicionado)
- **Buzzer:** Alarme sonoro
- **LEDs RGB:** Indicadores visuais (verde/amarelo/vermelho)
- **LCD 16x2 I2C:** Display de informações

### Controle
- **Push Button:** Alternância modo manual/automático

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
| 🔴 Crítico | Vermelho | Ativado | temp > setpoint + 5°C |

### Modo Manual
- Pressionar botão desliga relé (segurança)
- Sistema mantém monitoramento de sensores
- Pressionar novamente retorna ao automático

---

## 🚀 Como Simular no Wokwi

### Opção 1: Link Direto
🔗 **[Abrir projeto no Wokwi](https://wokwi.com/projects/XXXXXXX)** *(atualizar após upload)*

### Opção 2: Importar Manualmente
1. Acesse [Wokwi.com](https://wokwi.com)
2. New Project → ESP32 → MicroPython
3. Copie os arquivos de `src/wokwi/`:
   - `diagram.json` → Aba "diagram.json"
   - `main.py` → Aba "main.py"
4. Start Simulation ▶️

---

## 📖 Documentação

- [Relatório Completo](docs/relatorio.md)
- [Roteiro da Apresentação](docs/apresentacao.md)
- [Referências Bibliográficas](docs/referencias.md)

---

## 👥 Equipe

- **[SEU NOME]** - Desenvolvimento de hardware e código
- **Kevin** - Documentação e testes

**Disciplina:** Sistemas Embarcados  
**Instituição:** [Nome da Universidade]  
**Data:** 12 de Janeiro de 2026

---

## 📜 Licença

Este projeto está sob a licença MIT - veja [LICENSE](LICENSE) para detalhes.

---

## 🙏 Agradecimentos

- Prof. [Nome do Professor] - Orientação técnica
- Wokwi - Plataforma de simulação
- Comunidade MicroPython

---

**⭐ Se este projeto foi útil, deixe uma estrela no GitHub!**
