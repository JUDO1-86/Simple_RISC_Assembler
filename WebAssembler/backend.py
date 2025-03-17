from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/assemble": {"origins": "http://127.0.0.1:3000"}})

opcode_mapping = {
    'ADD': '00000', 'SUB': '00001', 'MUL': '00010', 'DIV': '00011', 'MOD': '00100', 'CMP': '00101',
    'AND': '00110', 'OR': '00111', 'NOT': '01000', 'MOV': '01001', 'LSL': '01010', 'LSR': '01011',
    'ASR': '01100', 'NOP': '01101', 'LD': '01110', 'ST': '01111', 'BEQ': '10000', 'BGT': '10001',
    'B': '10010', 'CALL': '10011', 'RET': '10100'
}

def validate_register(register):
    """Ensure register is within R1-R16 (case-insensitive)"""
    print(f"Validating register: {register}")  # Debugging

    register = register.upper()  # Convert to uppercase 

    if not (register.startswith('R') and register[1:].isdigit()):
        raise ValueError(f"Invalid register format: {register}")

    reg_num = int(register[1:])
    if reg_num < 1 or reg_num > 16:  # Allow only R1-R16
        raise ValueError(f"Register {register} out of bounds (must be R1-R16)")
    
    binary_representation = format(reg_num - 1, '04b')
    print(f"Register {register} -> Binary: {binary_representation}")  # Debugging

    return binary_representation


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

    branch_2 = {'ADD','SUB','MUL','DIV','MOD','AND','OR','LSL','LSR','ASR'}
    branch_3 = {'NOT','MOV'}
    branch_4 = {'LD','ST'}
    branch_5 = {'NOP','RET'}
    branch_6 = {'CMP'}

    # Branch Instructions (CALL, B, BEQ, BGT)
    if asm[0].upper() in {'CALL', 'B', 'BEQ', 'BGT'}:
       target = asm[1]
       if target in label_dict:  # If the target is a label
       # Calculate relative address as offset from the current line number
          target_address = label_dict[target] - (line_number + 1)
       elif target.isdigit():  # If the target is a direct address
          target_address = int(target)
       else:
          raise ValueError(f"Undefined label or invalid address '{target}'")
       # Convert the target address to a 27-bit two's complement binary value
       if target_address < 0:
          imm_val = format((1 << 27) + target_address, '027b')  # Two's complement for negative values
       else:
          imm_val = format(target_address, '027b')

       return opcode + imm_val

    elif asm[0].upper() in branch_2:
        print(f"Parsing arithmetic instruction: {instruction}")  # Debugging

        if len(asm) == 4:
          dest_register = validate_register(asm[1])
          source_reg1 = validate_register(asm[2])

          if asm[3].isdigit():
            immediate_flag = '1'
            imm_val = format(int(asm[3]), '018b')
            print(f"Immediate value detected: {imm_val}")  # Debugging
            return opcode + immediate_flag + dest_register + source_reg1 + imm_val
          else:
            source_reg2 = validate_register(asm[3])
            print(f"Registers -> Dest: {dest_register}, Src1: {source_reg1}, Src2: {source_reg2}")  # Debugging
            return opcode + '0' + dest_register + source_reg1 + source_reg2 + '0' * 14

    elif asm[0].upper() in branch_3:
        dest_register = validate_register(asm[1])

        if asm[2].isdigit():
            immediate_flag = '1'
            imm_val = format(int(asm[2]), '018b')
            return opcode + immediate_flag + dest_register + '0' * 4 + imm_val
        else:
            source_reg2 = validate_register(asm[2])
            return opcode + '0' + dest_register + '0' * 4 + source_reg2 + '0' * 14

    elif asm[0].upper() in branch_4:
        if len(asm) == 4:
            dest_register = validate_register(asm[1])
            source_reg1 = validate_register(asm[2])

            if asm[3].isdigit():
                immediate_flag = '1'
                imm_val = format(int(asm[3]), '04b')
                return opcode + immediate_flag + dest_register + source_reg1 + imm_val + '0' * 14
            else:
                source_reg2 = validate_register(asm[3])
                return opcode + '0' + dest_register + source_reg1 + source_reg2 + '0' * 14

    elif asm[0].upper() in branch_5:
        return opcode + '0'*27

    elif asm[0].upper() in branch_6:
        if len(asm) == 3:
            source_reg1 = validate_register(asm[1])

            if asm[2].isdigit():
                immediate_flag = '1'
                imm_val = format(int(asm[2]), '018b')
                return opcode + immediate_flag + '0' * 4 + source_reg1 + imm_val
            else:
                source_reg2 = validate_register(asm[2])
                return opcode + '0' + source_reg1 + source_reg2 + '0' * 14

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
    app.run(port=8080, debug=True)
