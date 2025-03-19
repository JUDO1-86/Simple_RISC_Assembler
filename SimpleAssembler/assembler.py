import sys
def assemble_instruction(instruction,label_dict,line_number):
    """Convert a SimpleRISC instruction into 32-bit machine code."""
    opcode_mapping = {
        'ADD': '00000', 'SUB': '00001', 'MUL': '00010', 'DIV': '00011', 'MOD': '00100', 'CMP': '00101',
        'AND': '00110', 'OR': '00111', 'NOT': '01000', 'MOV': '01001', 'LSL': '01010', 'LSR': '01011',
        'ASR': '01100', 'NOP': '01101', 'LD': '01110', 'ST': '01111', 'BEQ': '10000', 'BGT': '10001',
        'B': '10010', 'CALL': '10011', 'RET': '10100'
    }
    asm = instruction.strip().split()
    # split suppose add r1 r2 5 then it shows as parts = ['ADD', 'R1', 'R2', '5']
    # Splits the instruction into a list of words based on spaces.

    if asm[0].endswith(':'):
        label_name = asm[0][:-1]  # Remove the colon
        label_dict[label_name] = line_number #creating the word label name and stroing its vale as line number
        return None

    if not asm:
        return None
    opcode = opcode_mapping.get(asm[0].upper(),None)
    if opcode is None:
        raise ValueError(f"error in instruction = {asm[0]}")

    branch_1 = {'CALL','B','BEQ','BGT'}
    branch_2 = {'ADD','SUB','MUL','DIV','MOD','AND','OR','LSL','LSR','ASR'}
    branch_3 = {'NOT','MOV'}
    branch_4 = {'LD','ST'}
    branch_5 = {'NOP','RET'}
    branch_6 = {'CMP'}

    if asm[0].upper() in {'CALL', 'B', 'BEQ', 'BGT'}:
        target = asm[1]
        if target in label_dict:
            target_address = label_dict[target]
        elif target.isdigit():
            target_address = int(target)
        else:
            raise ValueError(f"Error: Undefined label or invalid address '{target}'")

        imm_val = format(target_address, '027b')
        return opcode + imm_val

    elif asm[0].upper() in branch_2:
    # branch_2 = {'ADD','SUB','MUL','DIV','MOD','AND','OR','LSL','LSR','ASR'}
        if not asm[0].endswith(':'):
            if len(asm) == 4:
                if not asm[1][1:].isdigit():
                    raise ValueError(f"error in destination register = {asm[1]}")
                if not asm[2][1:].isdigit():
                    raise ValueError(f"error in source register 1 = {asm[2]}")

                elif asm[3].isdigit():
                    immediate_flag = '1'
                    dest_register = format(int(asm[1][1:]), '04b')
                    source_reg1 = format(int(asm[2][1:]), '04b')
                    imm_val = format(int(asm[3]), '018b')
                    return opcode + immediate_flag + dest_register + source_reg1 + imm_val
                else:
                    if not asm[3].isdigit():
                        immediate_flag = '0'
                        dest_register = format(int(asm[1][1:]), '04b')
                        source_reg1 = format(int(asm[2][1:]), '04b')
                        source_reg2 = format(int(asm[3][1:]), '04b')
                        return opcode + immediate_flag + dest_register + source_reg1 + source_reg2 + '0' * 14
                    else:
                        raise ValueError(f"error in source register 2 = {asm[3]}")
        elif asm[0].endswith(':'):
            if len(asm) == 4:
                if not asm[1][1:].isdigit():
                    raise ValueError(f"error in destination register = {asm[1]}")
                if not asm[2][1:].isdigit():
                    raise ValueError(f"error in source register 1 = {asm[2]}")

                elif asm[3].isdigit():
                    immediate_flag = '1'
                    dest_register = format(int(asm[1][1:]), '04b')
                    source_reg1 = format(int(asm[2][1:]), '04b')
                    imm_val = format(int(asm[3]), '018b')
                    return opcode + immediate_flag + dest_register + source_reg1 + imm_val
                
                else:
                    raise ValueError(f"error in source register 2 = {asm[3]}")

            else:
                raise ValueError(f"error in instruction = {instruction}")

    elif asm[0].upper() in branch_3: #  branch_3 = {'NOT','MOV'}

         if not asm[1][1:].isdigit():
             raise ValueError(f"error in instruction = {asm[1]}")

         if asm[2].isdigit():
                immediate_flag = '1'
                dest_register = format(int(asm[1][1:]), '04b')
                imm_val = format(int(asm[2]), '018b')
                return opcode + immediate_flag + dest_register + '0' * 4 + imm_val

         elif asm[2][1:].isdigit():
                immediate_flag = '0'
                dest_register = format(int(asm[1][1:]), '04b')
                source_reg2 = format(int(asm[2][1:]), '04b')
                return opcode + immediate_flag + dest_register + '0' * 4 + source_reg2 + '0' * 14
         else :
             raise ValueError(f"eror in r2/imm value = {asm[2]}")

    elif asm[0].upper() in branch_4: #branch_4 = {'LD','ST'}
        if len(asm) == 4:

            if asm[3].isdigit():
                immediate_flag = '1'
                dest_register = format(int(asm[1][1:]), '04b')
                source_reg1 = format(int(asm[2][1:]), '04b')
                imm_val = format(int(asm[3]), '04b')
                return opcode + immediate_flag + dest_register + source_reg1 + imm_val + '0' * 14
            elif asm[3][1:].isdigit():
                immediate_flag = '0'
                dest_register = format(int(asm[1][1:]), '04b')
                source_reg1 = format(int(asm[2][1:]), '04b')
                source_reg2 = format(int(asm[3][1:]), '04b')
                return opcode + immediate_flag + dest_register + source_reg1 + source_reg2 + '0' * 14
            else :
                raise ValueError(f"error in rs2/imm value = asm[3]")

        else:
            raise ValueError(f"error in instruction  =  {instruction}")

    elif asm[0].upper() in branch_5:  # branch_5 = {'NOP','RET'}

        return opcode + '0'*27

    elif asm[0].upper() in branch_6:   # branch_6 = {'CMP'}
        if len(asm) == 3:
            if asm[2].isdigit():
                immediate_flag = '1'
                source_reg1 = format(int(asm[1][1:]), '04b')

                imm_val = format(int(asm[2]), '018b')
                return opcode + immediate_flag +'0'*4 + source_reg1 + imm_val
            else:
                immediate_flag = '0'

                source_reg1 = format(int(asm[1][1:]), '04b')
                source_reg2 = format(int(asm[2][1:]), '04b')
                return opcode + immediate_flag + '0'*4 + source_reg1 + source_reg2 + '0' * 14
        else:
            raise ValueError(f"error in instruction = {instruction}")

def assemble_file(input_file, output_file):
    """Read an assembly file and write the machine code output."""
    label_dict = {}  # Dictionary to store label addresses
    instructions = []  # List to store all instructions

    # First pass: Identify labels and store their addresses
    with open(input_file, 'r') as infile:
        for line_num, line in enumerate(infile):
            line = line.split('#')[0].strip()  # Remove comments
            if line:
                asm = line.split()
                if asm[0].endswith(':'):
                    label_name = asm[0][:-1]  # Remove the colon
                    label_dict[label_name] = len(instructions)  # Store line index
                else:
                    instructions.append(line)  # Store the line for second pass

    # Second pass: Convert assembly to binary
    with open(output_file, 'w') as outfile:
        for line_num, line in enumerate(instructions):
            try:
                binary_code = assemble_instruction(line, label_dict, line_num)
                if binary_code:
                    outfile.write(binary_code + '\n')
            except ValueError as e:
                print(f"Error: {e}")

    print(f" output written to {output_file}")


def main():
    if len(sys.argv) != 3:
        print("Usage: python assembler.py input.asm output.bin")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    assemble_file(input_file, output_file)


if __name__ == "__main__":
    main()
