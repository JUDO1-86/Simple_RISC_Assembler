# **SimpleRISC Assembler**  

This project implements an assembler for the **SimpleRISC** architecture. It provides both a **graphical interface** and a **command-line version**, allowing users to convert assembly instructions into **binary machine code**. This serves as an **educational tool** to understand how an assembler processes source code and generates machine instructions.  

## **Project Members**  

👥 **Contributors:**  
1️⃣ **Kiran Kumar Bommu** - 2302VL03  
2️⃣ **Vinay Kethavath** - 2302CM04  
3️⃣ **Karthik Gandam** - 2302VL09  
4️⃣ **Naveen Reddy** - 2302VL04  
5️⃣ **Rahul Rathod** - 2302VL06  

---

## **Project Structure**  

```
Simple_RISC_Assembler/
│
├── GUI_Assembler/
│   ├── Frontend.html
│   ├── backend.py
│   ├── requirements.txt
│
├── SimpleAssembler/
│   ├── assembler.py
│   ├── input.asm
│   ├── output.bin
│
├── README.md
├── Rules.txt

```  

---

## **Features**  

✔ **Supports arithmetic, logical, branch, and memory instructions**  
✔ **Handles labels for branching and function calls**  
✔ **Provides a GUI and CLI version for ease of use**  
✔ **Converts SimpleRISC assembly into binary machine code**  

---

## **Getting Started**  

### **Prerequisites**  

To run the GUI-based assembler:  
- **Python 3.x** installed  
- **Flask** (for backend)  

To use the command-line assembler:  
- Python 3.x  

---

## **Setup and Usage**  

### **Using the GUI Assembler**  
You can access the GUI Assembler through this link  
https://judo1-86.github.io/Frontend-assembler/ 

![Screenshot 2025-03-19 151525](https://github.com/user-attachments/assets/daf0466e-afc9-4337-8636-31bfb3e97a30)

---

### **Using the Command-Line Assembler**  
1. Navigate to the **SimpleAssembler** directory:  
   ```sh
   cd SimpleAssembler  
   ```  
2. Assemble an input file:  
   ```sh
   python assembler.py input.asm output.bin  
   ```  

---

## **Supported Instructions**  

### **Arithmetic & Logical**  
✅ ADD, SUB, MUL, DIV, MOD, AND, OR, CMP, NOT, MOV  

### **Shift Operations**  
✅ LSL, LSR, ASR  

### **Branching**  
✅ B, BEQ, BGT, CALL, RET  

### **Memory Access**  
✅ LD, ST  

### **Other**  
✅ NOP  

---

## **Limitations**  

⚠ **Registers are assumed to be in the format `R<number>` but lack range checks.**  
⚠ **No validation for immediate value range.**
## **Please follow the rules for getting ouput correctly **

---
