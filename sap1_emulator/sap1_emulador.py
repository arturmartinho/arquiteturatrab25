class SAP1:
    def __init__(self):
        self.reset()

    def reset(self):
        self.memory = [0] * 16
        self.pc = 0      
        self.ir = 0      
        self.mar = 0     
        self.acc = 0      
        self.b = 0      
        self.out = 0     
        self.halted = False
        self.carry_flag = False
        self.zero_flag = False

    def load_program(self, program):
        self.reset()
        for i, instr in enumerate(program):
            self.memory[i] = instr

    def fetch(self):
        if self.pc >= len(self.memory):
            self.halted = True
            return
        self.mar = self.pc
        self.ir = self.memory[self.mar]
        self.pc += 1

    def decode_execute(self):
        opcode = (self.ir & 0xF0) >> 4
        addr = self.ir & 0x0F

        # Opcodes e lógica:
        if opcode == 0x0:  # NOP
            pass

        elif opcode == 0x1:  # LDA addr
            self.acc = self.memory[addr]
            self.update_flags(self.acc)

        elif opcode == 0x2:  # ADD addr
            self.b = self.memory[addr]
            result = self.acc + self.b
            self.carry_flag = result > 0xFF
            self.acc = result & 0xFF
            self.update_flags(self.acc)

        elif opcode == 0x3:  # SUB addr
            self.b = self.memory[addr]
            result = self.acc - self.b
            self.carry_flag = result < 0
            self.acc = result & 0xFF
            self.update_flags(self.acc)

        elif opcode == 0x4:  # STA addr
            self.memory[addr] = self.acc

        elif opcode == 0x5:  # LDI value (load imediato)
            self.acc = addr
            self.update_flags(self.acc)

        elif opcode == 0x6:  # JMP addr
            self.pc = addr

        elif opcode == 0x7:  # JC addr (jump if carry)
            if self.carry_flag:
                self.pc = addr

        elif opcode == 0x8:  # JZ addr (jump if zero)
            if self.zero_flag:
                self.pc = addr

        elif opcode == 0xE:  # OUT
            self.out = self.acc

        elif opcode == 0xF:  # HLT
            self.halted = True

        else:
            raise Exception(f"Instrução inválida com opcode {opcode:X}")

    def update_flags(self, value):
        self.zero_flag = (value == 0)
        # carry_flag já tratado nas operações de soma/subtração

    def step(self):
        if self.halted:
            return
        self.fetch()
        if self.halted:
            return
        self.decode_execute()
