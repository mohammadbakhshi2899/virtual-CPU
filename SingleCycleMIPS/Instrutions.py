#these are our Instruction definition
instruction = {
    '000000100000':{
        'Type':'R',
        'Function' : 'add',
    },
    '000000100010':{
        'Type':'R',
        'Function':'sub',
    },
    '000000101010':{
        'type' : 'R',
        'Function' : 'slt',
    },
    '000000011010':{
        'type' : 'R',
        "Function" : 'div'
    },
    '000000011000':{
        'type' : 'R',
        "Function" : 'mult'
    },
    '000000010010':{
        'type' : 'R',
        "Function" : 'mflo'
    },
    '000000010000':{
        'type' : 'R',
        "Function" : 'mfhi'
    },
    '001000':{
        'Type':'I',
        'Function':'addi',
    },
    '001010':{
        'Type':'I',
        'Function':'slti',
    },
    '000100':{
        'Type':'J',
        'Function':'beq',
    },
    '000101':{
        'Type':'J',
        'Function':'bne',
    },
    '000010':{
        'Type':'J',
        'Function':'j',
    },
    '100011':{
        'Type':'I',
        'Function':'lw',
    },
    '101011':{
        'Type':'I',
        'Function':'sw',
    }
}

instruction_out_in = ['add', 'sub', 'slt', 'addi', 'slti', 'lw']
instruction_out_only = ['mflo', 'mfhi']
instruction_in_only = ['mult', 'div', 'beq', 'bne', 'j', 'sw']

pc = {
    'pc' : 0
}


