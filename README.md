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
GUI_Assembler/  
│── Frontend.html        # Web-based GUI for the assembler  
│── backend.py           # Backend processing for the GUI  
│  
SimpleAssembler/  
│── assembler.py         # Command-line assembler implementation  
│── input.asm            # Sample input assembly file  
│── output.bin           # Generated binary machine code  
│  
README.md                # Project documentation  
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
1. Clone the repository:  
   ```sh
   git clone https://github.com/JUDO1-86/Simple_RISC_Assembler.git
   cd Assembler
   ```  
2. Run the backend:  
   ```sh
   python backend.py  
   ```  
3. Open `Frontend.html` in a browser.  

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

---
