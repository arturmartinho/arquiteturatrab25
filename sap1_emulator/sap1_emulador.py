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

        if opcode == 0x0:    # NOP
            pass
        elif opcode == 0x1:  # LDA addr
            self.acc = self.memory[addr]
        elif opcode == 0x2:  # ADD addr
            self.b = self.memory[addr]
            self.acc = (self.acc + self.b) & 0xFF
        elif opcode == 0xE:  # OUT
            self.out = self.acc
        elif opcode == 0xF:  # HLT
            self.halted = True

    def step(self):
        if self.halted:
            return
        self.fetch()
        if self.halted:
            print("Halted após fetch")
            return
        print(f"Executando IR={self.ir:02X} PC={self.pc:02X} ACC={self.acc:02X}")
        self.decode_execute()
        print(f"Após exec: ACC={self.acc:02X} OUT={self.out:02X}")

