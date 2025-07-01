import tkinter as tk
from tkinter import messagebox
from sap1_emulador import SAP1
from montador import montar

class SAP1GUI:
    def __init__(self, master):
        self.master = master
        master.title("SAP-1 Emulator")
        master.configure(bg="#121212")
        master.resizable(False, False)

        self.sap = SAP1()
        self.create_widgets()
        self.update_ui()

    def create_widgets(self):
        font = ("Courier", 12, "bold")
        neon = "#00ffe1"
        accent = "#1f1f1f"
        label_bg = "#1a1a1a"

        # Frame estilo calculadora principal
        calc_frame = tk.Frame(self.master, bg="#121212")
        calc_frame.grid(row=0, column=0, padx=20, pady=20)

        # Frame superior - Registradores
        reg_frame = tk.Frame(calc_frame, bg="#121212")
        reg_frame.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        self.reg_labels = {}
        for i, reg in enumerate(["PC", "IR", "MAR", "ACC", "B", "OUT"]):
            lbl = tk.Label(reg_frame, text=f"{reg}: 00", fg=neon, bg=label_bg, font=font, width=10, pady=4, relief="ridge", bd=2)
            lbl.grid(row=0, column=i, padx=4)
            self.reg_labels[reg] = lbl

        # Memória
        self.mem_label = tk.Label(calc_frame, text="", fg="#72d5ff", bg="#121212", font=("Courier", 10), justify="left")
        self.mem_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0,10))

        # Código ASM
        code_frame = tk.Frame(calc_frame, bg="#121212")
        code_frame.grid(row=2, column=0, columnspan=2, pady=(0,10))
        self.asm_text = tk.Text(code_frame, height=6, width=50, bg="#101010", fg=neon,
                                insertbackground="white", font=font, bd=2, relief="groove")
        self.asm_text.grid(row=0, column=0, columnspan=2)
        self.asm_text.insert(tk.END, "; Digite seu código aqui\nLDA 14\nADD 15\nOUT\nHLT\n")

        # Entradas de memória
        input_frame = tk.Frame(calc_frame, bg="#121212")
        input_frame.grid(row=3, column=0, pady=(0,10))
        self.mem_entries = {}
        for i, label in enumerate([14, 15]):
            tk.Label(input_frame, text=f"Mem[{label}]", fg=neon, bg="#121212", font=font).grid(row=0, column=2*i)
            entry = tk.Entry(input_frame, width=4, font=font, fg="#0f0", bg=label_bg, insertbackground="white", relief="sunken")
            entry.grid(row=0, column=2*i+1, padx=5)
            entry.insert(0, "0")
            self.mem_entries[label] = entry

        # Botões estilo calculadora
        button_frame = tk.Frame(calc_frame, bg="#121212")
        button_frame.grid(row=3, column=1, sticky="e")

        def neon_button(text, command):
            return tk.Button(button_frame, text=text, command=command,
                             font=font, bg=accent, fg=neon, activebackground="#333", relief="raised",
                             bd=3, padx=12, pady=6, width=8)

        neon_button("⚙ Montar", self.montar_programa).grid(row=0, column=0, padx=5, pady=5)
        neon_button("▶ Run", self.run_program).grid(row=0, column=1, padx=5, pady=5)
        neon_button("⏭ Step", self.step).grid(row=0, column=2, padx=5, pady=5)
        neon_button("⭯ Reset", self.reset).grid(row=0, column=3, padx=5, pady=5)

        # OUT decimal
        self.out_label = tk.Label(calc_frame, fg="#ffff00", bg="#121212", font=("Courier", 14, "bold"))
        self.out_label.grid(row=4, column=0, pady=10, sticky="w")

        # Log (campo maior para facilitar visualização)
        self.log_text = tk.Text(calc_frame, height=15, width=80, font=("Courier", 10),
                                bg="#131419", fg="#00ff88", bd=2, relief="groove", insertbackground="white")
        self.log_text.grid(row=5, column=0, columnspan=2, pady=10)
        self.log_text.insert(tk.END, "Log de execução:\n")
        self.log_text.config(state=tk.DISABLED)

    def montar_programa(self):
        codigo_asm = self.asm_text.get("1.0", tk.END)
        try:
            programa = montar(codigo_asm)
            self.sap.load_program(programa)

            for addr, entry in self.mem_entries.items():
                try:
                    val = int(entry.get()) & 0xFF
                    self.sap.memory[addr] = val
                except:
                    self.sap.memory[addr] = 0

            self.sap.pc = 0
            self.sap.halted = False
            self.sap.out = 0

            self.update_ui()
            self.clear_log()
            messagebox.showinfo("Sucesso", "Programa montado e carregado com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def step(self):
        if self.sap.halted:
            messagebox.showinfo("Parado", "O programa já terminou (HLT).")
            return

        # Estado antes do passo
        pc_before = self.sap.pc
        ir_before = self.sap.ir
        acc_before = self.sap.acc
        b_before = self.sap.b
        mar_before = self.sap.mar
        out_before = self.sap.out
        carry_before = getattr(self.sap, "carry_flag", None)
        zero_before = getattr(self.sap, "zero_flag", None)

        # Passo da CPU (fetch + decode + execute)
        self.sap.step()

        # Estado depois do passo
        pc_after = self.sap.pc
        ir_after = self.sap.ir
        acc_after = self.sap.acc
        b_after = self.sap.b
        mar_after = self.sap.mar
        out_after = self.sap.out
        carry_after = getattr(self.sap, "carry_flag", None)
        zero_after = getattr(self.sap, "zero_flag", None)

        # Decodificar opcode e operando
        opcode = (ir_after & 0xF0) >> 4
        operando = ir_after & 0x0F

        opcode_map = {
            0x0: "NOP", 0x1: "LDA", 0x2: "ADD", 0x3: "SUB",
            0x4: "STA", 0x5: "LDI", 0x6: "JMP", 0x7: "JC",
            0x8: "JZ", 0xE: "OUT", 0xF: "HLT"
        }

        instr_name = opcode_map.get(opcode, "???")

        log_msg = (
            "----------------------------------------\n"
            f"PASSO EXECUTADO:\n"
            f"Instrução: {instr_name} {operando if instr_name not in ['NOP', 'OUT', 'HLT'] else ''}\n\n"

            "ESTADO ANTES DA INSTRUÇÃO:\n"
            f" PC  = 0x{pc_before:02X}\n"
            f" IR  = 0x{ir_before:02X}\n"
            f" MAR = 0x{mar_before:02X}\n"
            f" ACC = 0x{acc_before:02X}\n"
            f" B   = 0x{b_before:02X}\n"
            f" Flags:\n"
            f"  Carry = {carry_before}\n"
            f"  Zero  = {zero_before}\n\n"

            "ESTADO DEPOIS DA INSTRUÇÃO:\n"
            f" PC  = 0x{pc_after:02X}\n"
            f" IR  = 0x{ir_after:02X}\n"
            f" MAR = 0x{mar_after:02X}\n"
            f" ACC = 0x{acc_after:02X}\n"
            f" B   = 0x{b_after:02X}\n"
            f" Flags:\n"
            f"  Carry = {carry_after}\n"
            f"  Zero  = {zero_after}\n"
            "----------------------------------------"
        )

        self.log(log_msg)

        # Mostrar saída OUT somente se a instrução executada foi OUT
        if opcode == 0xE:
            self.log(f"SAÍDA (OUT): {out_after} (decimal)  |  0x{out_after:02X} (hexadecimal)")

        # Atualizar a interface gráfica
        self.update_ui()

    def run_program(self):
        if self.sap.halted:
            messagebox.showinfo("Fim", "Programa já terminou. Faça reset para rodar novamente.")
            return
        self.step()
        if not self.sap.halted:
            self.master.after(400, self.run_program)

    def reset(self):
        self.sap.reset()
        self.update_ui()
        self.clear_log()

    def update_ui(self):
        for reg in self.reg_labels:
            val = getattr(self.sap, reg.lower()) if reg != "OUT" else self.sap.out
            self.reg_labels[reg].config(text=f"{reg}: {val:02X}")

        mem_dump = "Memória:\n" + "  ".join(f"{i:02X}:{v:02X}" for i, v in enumerate(self.sap.memory))
        self.mem_label.config(text=mem_dump)

        self.out_label.config(text=f"OUT (decimal): {self.sap.out}")

    def clear_log(self):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete("1.0", tk.END)
        self.log_text.insert(tk.END, "Log de execução:\n")
        self.log_text.config(state=tk.DISABLED)

    def log(self, text):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, text + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = SAP1GUI(root)
    root.mainloop()
