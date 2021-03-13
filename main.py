from Structure.EVM import EVM,EVM_stack,EVM_memory,EVM_storage

import os
import json
import logging
from Structure.Constant import OPCODE_TO_INSTR
from Structure.Transaction import Transaction

def load_opcodes(file_path:str) -> 'Dict':
    opcodes = {}
    with open(file_path,"r",encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip().split(" ")
            opcode = line[1]
            if len(line) > 2:
                args = int(line[-1],16)
            else:
                args = None
            opcodes[int(line[0],16)] = (opcode,args)
    return opcodes

def execute_init():
    f = open("./log/running/init.log","w",encoding="utf-8")
    opcodes = load_opcodes("./data/init.disassemble")
    
    tx_0 = Transaction(
        tx_hash="0x79a09f9843b1248b192ea05f36b60686d3ca5bbee7020f7431aed669131516c7",
        msg_caller="0x5dc12131e65b8f395ab11a2c4e6af717e1b179ba",
        msg_value=0,
        msg_input="0", # shield input
        timestamp="2018-08-19 14:50:21 UTC"
    )

    evm = EVM(
        Stack=EVM_stack(),
        Memory=EVM_memory(),
        Storage=EVM_storage({}),
        Transaction=tx_0
    )
    while True:
        opcode = opcodes[evm.pc][0]
        args = opcodes[evm.pc][1]
        
        f.write("stack:[%s]\nmemory:%s\nstorage:%s\n%s\n\n"%(str(evm.Stack),str(evm.Memory),str(evm.Storage),"="*10+str(evm.pc)+":"+str(opcodes[evm.pc])+"="*10))
        f.flush()

        if opcode in ["RETURN","STOP","REVERT"]:
            break
        evm.pc += 1
        if args is not None:
            args_bytes = int(opcode.lstrip("PUSH"))
            evm.pc += args_bytes

        evm.args = args
        eval_function = "evm.%s()"%opcode        
        eval(eval_function)

    f.close()

    with open("./log/storage_readwrite/storage_init.json","w",encoding="utf-8") as f:
        json.dump({"read":evm.readStorage,"write":evm.writeStorage},f,indent='\t')
    
    return evm.Storage

def execute_tx(storage:'EVM_storage',transaction:'Transaction',opcodes:'Dict',DEBUG_Point:int=0x0):
    logging.basicConfig(
        filename="./log/%s.log"%transaction.get("tx_hash"),
        filemode="a",
        level=logging.INFO
    )
    evm = EVM(
        Stack=EVM_stack(),
        Memory=EVM_memory(),
        Storage=storage,
        Transaction=transaction
    )
    tx_hash = transaction.get("tx_hash")

    logging.info("="*20+"Running Transaction %s"%tx_hash+"="*20)

    f = open("./log/running/%s.log"%tx_hash,"w",encoding="utf-8")
    
    while True:
        opcode = opcodes[evm.pc][0]
        args = opcodes[evm.pc][1]
        
        f.write("stack:[%s]\nmemory:%s\nstorage:%s\n%s\n\n"%(str(evm.Stack),str(evm.Memory),str(evm.Storage),"="*10+hex(evm.pc)+"_"+str(evm.pc)+":"+str(opcodes[evm.pc])+"="*10))
        f.flush()

        if opcode in ["RETURN","STOP","REVERT"]:
            break
        evm.pc += 1
        if args is not None:
            args_bytes = int(opcode.lstrip("PUSH"))
            evm.pc += args_bytes

        evm.args = args
        eval_function = "evm.%s()"%opcode        
        eval(eval_function)

    f.close()

    with open("./log/storage_readwrite/%s.json"%tx_hash,"w",encoding="utf-8") as f:
        json.dump({"read":evm.readStorage,"write":evm.writeStorage},f,indent='\t')

    with open("./log/storage/%s.json"%tx_hash,"w",encoding="utf-8") as f:
        f.write(str(evm.Storage))

    return evm.Storage

def mk_dirs():
    if not os.path.exists("./log/storage"):
        os.makedirs("./log/storage")
    
    if not os.path.exists("./log/storage_readwrite"):
        os.makedirs("./log/storage_readwrite")
    
    if not os.path.exists("./log/running"):
        os.makedirs("./log/running")

if __name__ == "__main__":
    mk_dirs()
    logging.basicConfig(
        filename="./log/init.log",
        filemode="a",
        level=logging.INFO
    )
    storage = execute_init()
    
    opcodes = load_opcodes("./data/game.disassemble")

    # Create Gameid 01
    tx_1 = Transaction(
        tx_hash="0xaa8fcdb649889f7f1b63c37f34902650ffb2faedea4b3c6b6630f251f8aedbd8",
        msg_caller="0x5dc12131e65b8f395ab11a2c4e6af717e1b179ba",
        msg_value=50000000000000000,
        msg_input="0xfe1f6a0bd579d4fe1e90a03d545e3d8c01dfc19c2ae3b26ad26ba994a1dec89a435a3dc00000000000000000000000000000000000000000000000000000000000000000",
        timestamp="2018-08-19 15:05:16 UTC"
    )

    storage_after_1 = execute_tx(
        storage=storage,
        transaction=tx_1,
        opcodes=opcodes
    )

    # Join Gameid 01
    tx_2 = Transaction(
        tx_hash="0xabd8b650c2cdab9699bcfd52f3b24b991dc4d2abf7b24f8618bf8c1801f7f8ce",
        msg_caller="0xa70e846b87366ac57cf78fb2222e1ca404ba5406",
        msg_value=50000000000000000,
        msg_input="0xca6649c50000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000a",
        timestamp="2018-08-19 15:09:02 UTC"
    )

    storage_after_2 = execute_tx(
        storage=storage_after_1,
        transaction=tx_2,
        opcodes=opcodes
    )

    # Reveal & Close Gameid 01
    tx_3 = Transaction(
        tx_hash="0x4e7d11c4a1e726aac1e09bb7306c226337fad8e91907302f58f21123ef3f0713",
        msg_caller="0x5dc12131e65b8f395ab11a2c4e6af717e1b179ba",
        msg_value=0,
        msg_input="0x9a42f3aa0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000001e3e0db1bcb49b1666382383bb70ade300f1668972fd67a628673ceb1a402bcda3",
        timestamp="2018-08-19 15:10:09 UTC"
    )

    storage_after_3 = execute_tx(
        storage=storage_after_2,
        transaction=tx_3,
        opcodes=opcodes
    )


    print()