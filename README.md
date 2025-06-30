# 💻 Emulador SAP-1 com Interface Gráfica e Tradutor Assembly

Este projeto é uma implementação personalizada de um emulador SAP-1 (Simple-As-Possible) com interface gráfica e animação dos blocos funcionais, desenvolvido como parte da disciplina Arquitetura de Computadores I.

---

## 📋 Descrição

A aplicação emula a execução de programas simples escritos em linguagem Assembly para a arquitetura SAP-1, permitindo:

- Edição do código Assembly diretamente na interface.
- Tradução automática para código de máquina (assembler embutido).
- Execução passo a passo ou completa do programa.
- Visualização animada dos blocos funcionais (PC, MAR, RAM, ALU, etc).
- Interface amigável e interativa desenvolvida com **Tkinter**.

---

## 🧠 Arquitetura Simulada

O SAP-1 simulado contém os seguintes componentes:

- **Program Counter (PC)**
- **Memory Address Register (MAR)**
- **Random Access Memory (RAM)**
- **Instruction Register (IR)**
- **Accumulator (ACC)**
- **B Register**
- **Arithmetic Logic Unit (ALU)**
- **Output Register**
- **Controle de Clock e Barramento**

---
## 👨‍💻 Autores

- Mateus Gonçalves
- Lucca Sander Frisso
- Artur Rizzi Martinho


## 🚀 Como Executar

### ✅ Requisitos

- Python 3.8 ou superior
- Tkinter (incluído no Python padrão)

### ▶️ Executando o Emulador

```bash
python interface.py
