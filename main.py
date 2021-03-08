def load_opcodes():
    opcodes = []
    with open("./data.txt","r",encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip().split(" ")
            opcode = line[1]
            if len(line) > 2:
                args = opcode[-1]
            else:
                args = None
            opcodes.append((opcode,args))
    return opcodes

def load_init():
    stack = [0,0,int('d579d4fe1e90a03d545e3d8c01dfc19c2ae3b26ad26ba994a1dec89a435a3dc0',16),0,int(0x2b8,16),0]
    memory = []
    storage = {}

    return stack,memory,storage

if __name__ == "__main__":
    opcodes = load_opcodes()
    stack,memory,storage = load_init()

    print()