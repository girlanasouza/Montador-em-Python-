import sys

instructions = {'add':0b1000, 'shr':0b1001, 'shl':0b1010, 'not':0b1011, 'and':0b1100, 
'or': 0b1101, 'xor':0b1110, 'cmp': 0b1111, 'ld': 0b0000, 'st': 0b0001, 'data': 0b0010,
'jmpr': 0b0011,'jmp': 0b0100,'jcaez': 0b0101,'clf': 0b0110}

registradores = {"r0":0b00, "r1":0b01, "r2":0b10, "r3":0b11}
hex_code = ['00' for i in range(256)]

indiceHexCode = 0

def processaLinha(linha): #está processando para opção de data
    
    global indiceHexCode
    linha = linha.strip().replace(",", " ").split()
    ins = linha.pop(0)
    ins = instructions[ins]
    rb = linha.pop(0)
    rb = registradores[rb]
    ins = (ins<<4)+rb
    ins = str(hex(ins))[2:]
    dd = linha.pop(0)[2:]
    hex_code[indiceHexCode] = ins 
    indiceHexCode+=1
    hex_code[indiceHexCode] = dd
    indiceHexCode+=1






def parse_input_file(asm_file):
    with open(asm_file, 'r') as f: #open and close, abrir arq para leitura
        for linha in f.readlines():
            processaLinha(linha)
            
        



# def write_outputfile(memory_file, hex_code):
#     with open(memory_file, 'w') as f: #se n existe cria
#         f.write('v3.0 hex word plain')
#         f.write(str(hex(hex_code)).split('x')[1])
#     print(str(hex(hex_code)).split('x')[1])


def main(asm_file, memory_file):
    lines = parse_input_file(asm_file)
    #print(instructions[lines[0][0]]) 
    #hex_code = instructions[lines[0][0]]
    #write_outputfile(memory_file, hex_code)



if __name__ == '__main__':

    assert len(sys.argv) == 3, 'invalid number of input  arguments'

    
    main(sys.argv[1], sys.argv[2])

    print(hex_code)

#gerar um matriz 16x16