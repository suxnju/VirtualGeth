from Structure.EVM import EVM,EVM_stack,EVM_memory,EVM_storage

import logging

def load_opcodes():
    opcodes = []
    with open("./data.txt","r",encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip("\n").split(" ")
            opcode = line[1]
            if len(line) > 2:
                args = int(line[-1],16)
            else:
                args = None
            opcodes.append((hex(int(line[0],16)),opcode,args))
    return opcodes

def load_init():
    stack = [0,0,int('0x5dc12131e65b8f395ab11a2c4e6af717e1b179ba',16),0,int('0x2b8',16),0]
    memory = {}
    storage = {
        0:int("0x5dc12131e65b8f395ab11a2c4e6af717e1b179ba",16),#ceoAddress
        1:int("0x5dc12131e65b8f395ab11a2c4e6af717e1b179ba",16),#cfoAddress
        2:int("0x5dc12131e65b8f395ab11a2c4e6af717e1b179ba",16),#cooAddress
        3:0,#newContractAddress
        4:0,#tip_total
        5:10000000000000000,#tip_rate
        6:0,#paused
        7:4,#payoff length 具体的payoff的映射还没有实现
        8:0,#games
        9:0,#gamesidsOf
        10:0,#maxgame
        11:30,#expireTime
    }

    return stack,memory,storage

if __name__ == "__main__":
    DEBUG_Point = 0x1005
    f = open("runing_log.py","w",encoding="utf-8")
    opcodes = load_opcodes()
    stack,memory,storage = load_init()
    evm = EVM(
        Stack=EVM_stack(stack),
        Memory=EVM_memory(memory),
        Storage=EVM_storage(storage)
    )
    for opcode in opcodes:
        f.write("\tstack:[%s]\n\tmemory:[%s]\n\tstorage:[%s]\n\n%s\n"%(str(evm.Stack),str(evm.Memory),str(evm.Storage),opcode))
        f.flush()
        if int(opcode[0],16) == DEBUG_Point:
            break
        evm.args = opcode[2]
        eval_function = "evm.%s()"%opcode[1]
        eval(eval_function)

    f.close()