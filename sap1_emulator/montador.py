def montar(codigo_asm):
    opcodes = {
        "NOP": 0x00,
        "LDA": 0x10,
        "ADD": 0x20,
        "SUB": 0x30,
        "STA": 0x40,
        "LDI": 0x50,
        "JMP": 0x60,
        "JC":  0x70,
        "JZ":  0x80,
        "OUT": 0xE0,
        "HLT": 0xF0
    }
    programa = []
    for linha in codigo_asm.splitlines():
        linha = linha.strip()
        if linha == "" or linha.startswith(";"):
            continue
        partes = linha.split()
        instr = partes[0].upper()
        if instr not in opcodes:
            raise Exception(f"Instrução inválida: {instr}")
        codigo = opcodes[instr]
        if instr in ["LDA", "ADD", "SUB", "STA", "LDI", "JMP", "JC", "JZ"]:
            if len(partes) < 2:
                raise Exception(f"Falta operando na instrução: {linha}")
            operando = int(partes[1])
            if operando < 0 or operando > 15:
                raise Exception(f"Operando fora do intervalo 0-15: {operando}")
            codigo |= operando & 0x0F
        programa.append(codigo)
    return programa
