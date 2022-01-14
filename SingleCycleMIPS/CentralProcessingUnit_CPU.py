from Instrutions import instruction, instruction_out_in, instruction_out_only, instruction_in_only, pc
from RegisterFile import Registers, ALU_register
from RAM import memory
import RAM


class CPU():
    clk = 30  # clock time which will be used for calculating ex time

    def ALU_Arithmetical_logical_Unit(self, Operation, D1, D2, offset=0):
        operation = Operation
        if operation == 'mult':
            ALU_register['high'] = D1 * D2
            ALU_register['low'] = D1 * D2

        if operation == 'and':
            if D1 and D2:
                return True
            return False

        elif operation == 'div':
            ALU_register['low'] = D1 / D2
            ALU_register['high'] = D1 % D2

        elif operation == 'slt':
            if D1 > D2:
                return 1
            return 0

        elif operation == 'slti':
            if D1 > D2:
                return 1
            return 0

        elif operation == 'add':
            # asdfmasd
            return D1 + D2

        elif operation == 'addi':
            # sdfasdf
            return D1 + D2

        elif operation == 'mflo':
            # sdafasdf
            return ALU_register['low']

        elif operation == 'mfhi':
            # asdfasd
            return ALU_register['high']

        elif operation == 'beq':
            # conditional Jump
            if D1 == D2:
                pc['pc'] = self.SignEx(offset)
            else:
                pc['pc'] = pc['pc'] + 1

        elif operation == 'bne':
            # conditional Jump
            if D1 != D2:
                self.setInstructionIndex(self.SignEx(offset))
                pc['pc'] = self.SignEx(offset)
            else:
                pc['pc'] = pc['pc'] + 1

        elif operation == 'j':
            # without condition
            pc['pc'] = self.SignEx(offset)

        elif operation == 'lw':
            # cal Address
            return D1 + D2

        elif operation == 'sw':
            # cal Address
            return D1 + D2

    def RF_R_RegisterFileRead(self, rs, rt=None, SignEx=False, offset_or_address=True):
        if rt == None:
            return Registers[rs]
        if SignEx:
            rt = self.SignEx(rt)
        if offset_or_address:
            return Registers[rs], Registers[rt]

        return Registers[rs], rt

    def SignEx(self, imm):
        return int(imm, 2)

    def RF_W_RegisterFileWrite(self, destination, Value):
        Registers[destination] = Value

    def DM_DataMemory(self, address, RF, R_or_W):
        if R_or_W == False:
            return memory[address]
        memory[address] = RF

    def CU_ContrllUnit(self, code):
        Opcode = code[0:6]
        # R type instruction opcode is 000000
        if int(Opcode, 2) == 0:  # this is R type
            function = code[26:32]
            Identifier = Opcode + function
            operation = instruction[Identifier]['Function']
            if operation in instruction_out_in:
                rs_address = code[6:11]
                rt_address = code[11:16]
                rs_value, rt_value = self.RF_R_RegisterFileRead(rs_address, rt_address)
                operation_result = self.ALU_Arithmetical_logical_Unit(operation, rs_value, rt_value)
                rd_address = code[16:21]
                self.RF_W_RegisterFileWrite(rd_address, operation_result)
                self.nextInstruction()
            elif operation in instruction_in_only:
                rs_address = code[6:11]
                rt_address = code[11:16]
                rs_value, rt_value = self.RF_R_RegisterFileRead(rs_address, rt_address)
                self.ALU_Arithmetical_logical_Unit(operation, rs_value, rt_value)
                self.nextInstruction()
            elif operation in instruction_out_only:
                rd_address = code[16:21]
                operation_result = self.ALU_Arithmetical_logical_Unit(operation, None, None)
                self.RF_W_RegisterFileWrite(rd_address, operation_result)
                self.nextInstruction()
            else:
                print("unsupported command ")  #

        else:  # code is not R type
            Type = instruction[Opcode]['Type']
            if Type == 'I':  # code is I type
                operation = instruction[Opcode]['Function']

                if operation in instruction_out_in:  # we gonna set signals
                    rs_address = code[6:11]
                    rt_address = code[11:16]
                    imm = code[16:32]
                    rs_value, offset = self.RF_R_RegisterFileRead(rs_address, imm, SignEx=True, offset_or_address=False)
                    operation_result = self.ALU_Arithmetical_logical_Unit(operation, rs_value, offset)
                    if operation == 'lw':
                        memory_address = str(operation_result)
                        operation_result = self.DM_DataMemory(memory_address, None, R_or_W=False)
                    self.RF_W_RegisterFileWrite(rt_address, operation_result)

                    self.nextInstruction()
                elif operation in instruction_in_only:  # SW is the only I only input instruction
                    rs_address = code[6:11]
                    rt_address = code[11:16]
                    imm = code[16:31]
                    rs_value, offset = self.RF_R_RegisterFileRead(rs_address, imm, SignEx=True, offset_or_address=False)
                    destinationAddress = self.ALU_Arithmetical_logical_Unit(operation, rs_value, offset)
                    rt_value = self.RF_R_RegisterFileRead(rt_address)
                    self.DM_DataMemory(destinationAddress, rt_value, R_or_W=True)
                    self.nextInstruction()
                else:
                    print("unsupported command ")
            elif Type == 'J':  # code is J type
                operation = instruction[Opcode]['Function']
                if operation == 'j':
                    offset = code[6:32]
                    self.ALU_Arithmetical_logical_Unit(operation, None, None, offset=offset)
                    self.PC_programCounter(pc["pc"])
                else:  # the operation either bne or beq # conditional jump
                    rs_address = code[6:11]
                    rt_address = code[11:16]
                    offset = code[16:32]
                    rs_value, rt_value = self.RF_R_RegisterFileRead(rs_address, rt_address)
                    self.ALU_Arithmetical_logical_Unit(operation, rs_value, rt_value, offset=offset)
                    self.PC_programCounter(pc["pc"])
            else:
                print("Unsupported code type")

    def IM_InstructionMemory(self, address):
        Instruction = RAM.codes[address].strip()
        self.CU_ContrllUnit(Instruction)

    def PC_programCounter(self, codeIndex):
        print(Registers)
        if codeIndex < len(RAM.codes):
            self.IM_InstructionMemory(codeIndex)
            print(codeIndex)
        else:
            print("the operation is done or out of index")

    def nextInstruction(self, changeSize=1):
        pc['pc'] = pc['pc'] + changeSize
        self.PC_programCounter(pc['pc'])

    def setInstructionIndex(self, index):
        pc['pc'] = index

    def giveProgramToExcute(self, addressFile, mode='singleCycle'):
        with open(addressFile, 'r+') as lines:
            codes = lines.readlines()
            RAM.codes = codes

    def start(self):
        print(RAM.codes)
        self.PC_programCounter(0)
