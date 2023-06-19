import sys
instructions_ari = {'add':0b1000, 'shr':0b1001, 'shl':0b1010, 'not':0b1011, 'and':0b1100, 
'or': 0b1101, 'xor':0b1110, 'cmp': 0b1111, 'ld': 0b0000, 'st': 0b0001}

instructions_data = {'data': 0b0010}

instructions_io = {'in':0b0111, 'out':0b0111}

instructions_clf = {'clf': 0b0110}

instructions_jmp={'jmpr': 0b0011,'jcaez': 0b0101,'jmp': 0b0100}

hex_code = ['00' for i in range(256)]

translater = {
        '0000': '0',
        '0001': '1',
        '0010': '2',
        '0011': '3',
        '0100': '4',
        '0101': '5',
        '0110': '6',
        '0111': '7',
        '1000': '8',
        '1001': '9',
        '1010': 'a',
        '1011': 'b',
        '1100': 'c',
        '1101': 'd',
        '1110': 'e',
        '1111': 'f',
    }
hex_to_dec = {'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'a':10,'b':11,'c':12,'d':13,'e':14, 'f':15}
registradores = {"r0":"00", "r1":'01', "r2":'10', "r3":'11'}

labels = {}
i_hex = 0

def ins_arithmetic(line):
    global i_hex
    instruction = line.pop(0)
    bin_value = instructions_ari[instruction] 
    hex_value = str(hex(bin_value))[2:] 
    ra = line.pop(0)
    rb = line.pop(0)
    ra= registradores[ra] 
    rb= registradores[rb] 
    s = translater[f'{ra}{rb}']
    hex_value = hex_value + s
    hex_code[i_hex]=hex_value
    i_hex+=1

def find_label(line):    
    ins = line[0]
    if ins.find(':'):
        return 1
    else:
        return 0

def indetify_jmp(ins): #c
    code = 0b01010000
    for character in ins[1:]:
        if character =='c':
            code+=0b1000
        elif character == 'a':
            code+=0b0100
        elif character == 'e':
            code+=0b0010
        elif character == 'z':
            code+=0b00001
    return code

def convertStrInBin(string):
    binValue = 0
    for i in range(0, len(string)):
        if(string[i] == '0'):
            binValue += 0       
        else:
            binValue += 1
        binValue = binValue >> 1
    return binValue

def convert_dec_hex(num):
    num = hex(int(num))[2:]
    return num

def comp_dois(num): 
    num = int(num)
    if num >= 0:
        return 0
    else:
        return hex(2**32 + num)[2:][-2:]  

def find_label_arq(hex_code):
    for i in range (len(hex_code)):
        if hex_code[i] in labels:
            hex_code[i] = labels[hex_code[i]]
 
def trater_instructions(line):
    global i_hex
    line = line.strip().replace(",", " ").split() 
    if line[0] == 'data':
        ins = line.pop(0) 
        ins = str(hex(instructions_data[ins]))[2:] 
        ra = line.pop(0)
        ra = registradores[ra] 
        ra = '00'+ra     
        ra = translater[ra] 
        hex_value = f'{ins}{ra}' 
        
        value = line.pop(0)
        
        if '-' in value:
       
            value = comp_dois(value) 
            
        elif value.isnumeric():
            value = convert_dec_hex(value).zfill(2)

        elif not '0x' in value and not value.isnumeric():
            if value not in labels:
                hex_code[i_hex]=hex_value
                i_hex+=1
                hex_code[i_hex]=value
                i_hex +=1
                return
            else:
                value = labels[value]
        else:
            value = value[2:]
        hex_code[i_hex]=hex_value
        i_hex+=1
        
        hex_code[i_hex]=value
        i_hex+=1
    #tratamento do clf
    elif line[0]=='clf':  
        ins = line.pop(0)
        ins = str(hex(instructions_clf[ins]))[2:]  + '0' 
        hex_code[i_hex]=ins
        i_hex+=1
    #tratamento de labels
    elif ':' in line[0]:
        ins = line.pop(0)[:-1]
        if ins in labels:
            hexNumber = str(hex(i_hex))[2:] 
            hexNumber = hexNumber if len(hexNumber) == 2 else f"0{hexNumber}" 
            pos = labels[ins][2:]
            pos = hex_to_dec[pos]
            hex_code[pos] = hexNumber                  
        else:

            hexNumber = str(hex(i_hex))[2:] #04
            hexNumber = hexNumber if len(hexNumber) == 2 else f"0{hexNumber}" 
            labels[ins]= hexNumber
    #tratamento do jump simples
    elif line[0] == 'jmp':      
        ins=line.pop(0)      
        ins = hex(instructions_jmp[ins])[2:]+'0'
        hex_code[i_hex] = ins
        i_hex+=1
        term = line.pop(0) 
        if '0x' in term:
            term=term[2:]
            hex_code[i_hex]=term
            i_hex+=1
        elif term.isdigit(): 
            term = (hex(int(term)))[2:].zfill(2)
            hex_code[i_hex]=term
            i_hex+=1
            
        elif term in labels:  
            term = labels[term]
            hex_code[i_hex]=term
            i_hex+=1
        else:
            hex_code[i_hex]=term
            i_hex+=1
            
    #tratatamento dos jump condicionado 
    elif ('j' in line[0]): 
        ins=line.pop(0) 
        code = str(hex(indetify_jmp(ins)))[2:]
        hex_code[i_hex]=code
        i_hex+=1
        term = line.pop(0)
        if '0x' in term:
            term=term[2:]
            hex_code[i_hex]=term
            i_hex+=1
        elif term.isdigit(): 
            term = (hex(int(term)))[2:].zfill(2)
            hex_code[i_hex]=term
            i_hex+=1

        elif term in labels:
            term = labels[term]
            hex_code[i_hex]=term
            i_hex+=1
            
        else:
            hex_code[i_hex]=term
            i_hex+=1
        
    #tratamento da jmpr
    elif line[0]=='jmpr':
        ins = line.pop(0)
        ins = str(instructions_jmp[ins])
        reg = line.pop(0)
        reg = registradores[reg]
        reg = '00'+reg
        reg = translater[reg]
        ins = ins + reg
        
    #tratamento do output
    elif line[0]=='out' or line[0]=='in':
        end=hex(instructions_io[line[0]])[2:] 
        ins = line.pop(0) 
        ir = line.pop(0) 
        rb = line.pop(0)
        rb = registradores[rb]
        if ins=='out':
            value_ins = '1'
            if ir=='addr':
                value_ins += '1'
            elif ir=='data':
                value_ins+='0'  
        elif ins=='in':
            value_ins ='0'
            if ir=='addr':
                value_ins += '1'
            elif ir=='data':
                value_ins+='0'
        
        value_ins = value_ins + rb
        value_ins = translater[value_ins]
        ins = end + value_ins  

        hex_code[i_hex]=ins
        i_hex+=1
        
    #tratamento dos aritmeticos  
    elif line[0] =='halt':
        hex_code[i_hex]='40'     
        pos=(hex(i_hex))[2:]
        if len(pos)==1:
            pos='0'+pos
        i_hex+=1
        hex_code[i_hex]=pos
        i_hex+=1
    
    elif(line[0]=='move'):
        ins = line.pop(0)  
        ra = line.pop(0)
        ra= registradores[ra]
        rb = line.pop(0)
        rb = registradores[rb]
        aux = rb
        ins = bin(instructions_ari['xor'])[2:]
        ins = translater[ins]  
        rb = rb + rb
        rb = translater[rb]
        ins = ins + rb

        hex_code[i_hex]=ins
        i_hex+=1

        ins = str(instructions_ari['add'])
        reg = translater[ra+aux] 
        ins = ins + reg
        hex_code[i_hex]=ins
        i_hex+=1

    elif('.' in line[0]):
        
        ins = line.pop(1)
        if '0x' in ins:
            ins= ins[2:]
        elif '-' in ins:
            ins = comp_dois(ins) 
        else:
            ins = hex(int(ins))[2:]
        if len(ins)==1:
            ins='0'+ins
        hex_code[i_hex]=ins
        i_hex+=1
    else:
        ins_arithmetic(line)

def parse_input_file(asm_file):
    with open(asm_file, 'r') as f: 
        for linha in f.readlines():
            if len(linha.strip()) > 0:
                trater_instructions(linha)
            

def write_outputfile(memory_file, hex_code): 
    with open(f'{memory_file}.m', 'w') as f:
        
        f.write('v3.0 hex words plain\n')
        tm = 0
        for i in range(16):
            for j in range(16):
               f.write(f"{hex_code[tm]}  ")
               tm += 1
            f.write('\n')

def main(asm_file, memory_file):
    lines = parse_input_file(asm_file)
    find_label_arq(hex_code)
    write_outputfile(memory_file, hex_code)


if __name__ == '__main__':
    assert len(sys.argv) == 3, 'invalid number of input  arguments'
    main(sys.argv[1], sys.argv[2])
