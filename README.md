# SimpleRISC Assembler

A basic assembler that converts SimpleRISC assembly language instructions into 32-bit machine code.

## Group Members 
1)Kiran Kumar Bommu-2302VL03
2)Vinay Kethavath-2302CM04
3)Karthik Gandam-2302VL09
4)Naveen Reddy-2302VL04
5)Rahul Rathod-230VL06

## Features
- Supports a set of arithmetic, logical, branch, and memory instructions.
- Handles labels for branching and function calls.
- Converts assembly to binary machine code.

## Usage

To assemble a SimpleRISC assembly file into machine code, use:

```sh
python assembler.py input.asm output.bin
```

### Example Assembly Code (input.asm)
```assembly
START:  ADD R1, R2, 5   # Add immediate value 5 to R2 and store in R1
        CMP R1, 10      # Compare R1 with 10
        BEQ END         # Branch to END if equal
        B START         # Unconditional branch to START
END:    NOP             # No operation
```

### Assembled Output (output.bin)
```
00000100010010000000000000000101
00101100000001000000000000001010
10000000000000000000000000000100
10010000000000000000000000000000
01101000000000000000000000000000
```

## Supported Instructions
- **Arithmetic & Logical**: ADD, SUB, MUL, DIV, MOD, AND, OR, CMP, NOT, MOV
- **Shift Operations**: LSL, LSR, ASR
- **Branching**: B, BEQ, BGT, CALL, RET
- **Memory Access**: LD, ST
- **Other**: NOP

## Limitations
- Registers are assumed to be in the format `R<number>` but lack range checks.
- No immediate value range validation.



