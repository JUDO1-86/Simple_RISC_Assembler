from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


opcode_mapping = {
    'ADD': '00000', 'SUB': '00001', 'MUL': '00010', 'DIV': '00011', 'MOD': '00100', 'CMP': '00101',
    'AND': '00110', 'OR': '00111', 'NOT': '01000', 'MOV': '01001', 'LSL': '01010', 'LSR': '01011',
    'ASR': '01100', 'NOP': '01101', 'LD': '01110', 'ST': '01111', 'BEQ': '10000', 'BGT': '10001',
    'B': '10010', 'CALL': '10011', 'RET': '10100'
}

def normalize_instruction(instruction):
    """Removes unnecessary spaces and normalizes instruction format."""
    return instruction.replace(',', ' ').strip()

def assemble_instruction(instruction, label_dict, line_number):
    """Convert a SimpleRISC instruction into 32-bit machine code."""
    asm = normalize_instruction(instruction).split()
    
    if not asm:
        return None

    if asm[0].endswith(':'):
        label_dict[asm[0][:-1]] = line_number
        return None

    opcode = opcode_mapping.get(asm[0].upper())
    if opcode is None:
        raise ValueError(f"Unknown instruction: {asm[0]}")
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
                    if not asm[3].isdigit():
                        immediate_flag = '0'
                        dest_register = format(int(asm[2][1:]), '04b')
                        source_reg1 = format(int(asm[3][1:]), '04b')
                        source_reg2 = format(int(asm[4][1:]), '04b')
                        return opcode + immediate_flag + dest_register + source_reg1 + source_reg2 + '0' * 14
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

         else:
                immediate_flag = '0'
                dest_register = format(int(asm[1][1:]), '04b')
                source_reg2 = format(int(asm[2][1:]), '04b')
                return opcode + immediate_flag + dest_register + '0' * 4 + source_reg2 + '0' * 14

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
                immediate_flag = '1'
                dest_register = format(int(asm[1][1:]), '04b')
                source_reg1 = format(int(asm[2][1:]), '04b')
                source_reg2 = format(int)

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
                return opcode + immediate_flag + source_reg1 + source_reg2 + '0' * 14
        else:
            raise ValueError(f"error in instruction = {instruction}") 

def assemble_code(assembly_code):
    label_dict = {}
    instructions = []
    output = []

    lines = assembly_code.split("\n")
    for line in lines:
        line = line.split('#')[0].strip()  # Remove comments
        if line:
            line = normalize_instruction(line)  # Fix spacing
            asm = line.split()
            if asm[0].endswith(':'):
                label_dict[asm[0][:-1]] = len(instructions)
                if len(asm) > 1:
                    instructions.append(" ".join(asm[1:]))  # Append instruction after label
            else:
                instructions.append(line)

    print("Parsed Instructions:", instructions)

    for line_num, line in enumerate(instructions):
        try:
            binary_code = assemble_instruction(line, label_dict, line_num)
            if binary_code:
                output.append(binary_code)
        except ValueError as e:
            return {"error": str(e)}

    print("Generated Machine Code:", output)

    return {"machine_code": output}
@app.route("/")
def home():
    return "Welcome to the Simple RISC Assembler API!"

@app.route('/assemble', methods=['POST'])
def assemble():
    """API Endpoint to assemble the code."""
    data = request.json

    if not data or 'code' not in data:
        return jsonify({"error": "No input provided"}), 400

    print("Received assembly code:", data['code'])

    result = assemble_code(data['code'])

    print("Returning result:", result)
    return jsonify(result)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)

