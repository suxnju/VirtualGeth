from Structure.EVM import EVM,EVM_stack,EVM_memory,EVM_storage

import os
import json
import logging
import pandas as pd
import math

from Structure.Constant import OPCODE_TO_INSTR
from Structure.Transaction import Transaction

from collections import Counter
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
    opcodes = load_opcodes("./data/init.disassemble")
    
    tx_0 = Transaction(
        tx_hash="0x79a09f9843b1248b192ea05f36b60686d3ca5bbee7020f7431aed669131516c7",
        msg_caller="0x5dc12131e65b8f395ab11a2c4e6af717e1b179ba",
        msg_value=0,
        msg_input="0", # mask input
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

        if opcode in ["RETURN","STOP","REVERT"]:
            break
        evm.pc += 1
        if args is not None:
            args_bytes = int(opcode.lstrip("PUSH"))
            evm.pc += args_bytes

        evm.args = args
        eval_function = "evm.%s()"%opcode        
        eval(eval_function)

    return evm.Storage, {"read":evm.readStorage,"write":evm.writeStorage}

def execute_tx(storage:'EVM_storage',transaction:'Transaction',opcodes:'Dict',DEBUG_Point:int=0x0,verbose:bool=False):
    evm = EVM(
        Stack=EVM_stack(),
        Memory=EVM_memory(),
        Storage=storage,
        Transaction=transaction
    )
    tx_hash = transaction.get("tx_hash")
    
    if verbose:
        f = open("./log/running/%s.log"%tx_hash,"w",encoding="utf-8")

    while True:
        opcode = opcodes[evm.pc][0]
        args = opcodes[evm.pc][1]

        if verbose:
            f.write("stack:[%s]\nmemory:%s\nstorage:%s\n%s\n\n"%(str(evm.Stack),str(evm.Memory),str(evm.Storage),"="*10+hex(evm.pc)+"_"+str(evm.pc)+":"+str(opcodes[evm.pc])+"="*10))

        if opcode in ["RETURN","STOP","REVERT"]:
            if opcode == "REVERT":
                print()
            break
        evm.pc += 1
        if args is not None:
            args_bytes = int(opcode.lstrip("PUSH"))
            evm.pc += args_bytes

        evm.args = args
        eval_function = "evm.%s()"%opcode        
        eval(eval_function)

    if verbose:
        f.close()
        with open("./log/storage_readwrite/%s.json"%tx_hash,"w",encoding="utf-8") as f:
            json.dump({"read":[v.rjust(64,"0") for v in evm.readStorage],"write":[v.rjust(64,"0") for v in evm.writeStorage]},f,indent='\t')

        with open("./log/storage/%s.json"%tx_hash,"w",encoding="utf-8") as f:
            f.write(str(evm.Storage))

    return evm.Storage, {"read":evm.readStorage,"write":evm.writeStorage}

def load_group(data_file="./data/game_group.csv") -> 'Dict':
    exec_txs = pd.read_csv(data_file,sep=',')
    group = {}
    for row, exec_tx in exec_txs.iterrows():
        if exec_tx['data'] not in group:
            group[exec_tx['data']] = [exec_tx['transaction_hash']]
        else:
            group[exec_tx['data']].append(exec_tx['transaction_hash'])
    
    return group

def load_data(data_file="./data/game_txs.csv") -> 'Transaction':
    exec_txs = pd.read_csv(data_file,sep=',').sort_values(by=['block_timestamp','transaction_index'],ascending=(True,True))
    for row, exec_tx in exec_txs.iterrows():
        if exec_tx['hash'] == "0x79a09f9843b1248b192ea05f36b60686d3ca5bbee7020f7431aed669131516c7": # init has executed
            continue
        if exec_tx['receipt_status'] == 0: # ignore failed transactions
            continue
        print("\r%d"%row,end='')
        yield Transaction(
            tx_hash=exec_tx['hash'],
            msg_caller=exec_tx['from_address'],
            msg_value=int(exec_tx['value']),
            msg_input=exec_tx['input'],
            timestamp=exec_tx['block_timestamp']
        )

def check_common_slot(groupid:int,txs:'list',storage_modified:'Dict') -> 'bool':
    commons = set()
    for i, tx_hash in enumerate(txs):
        if i == 0:
            commons = commons | set(storage_modified[tx_hash]['read'] + storage_modified[tx_hash]['write'])
        else:
            commons = commons & set(storage_modified[tx_hash]['read'] + storage_modified[tx_hash]['write'])

    return commons

def mk_dirs():
    if not os.path.exists("./log/storage"):
        os.makedirs("./log/storage")
    
    if not os.path.exists("./log/storage_readwrite"):
        os.makedirs("./log/storage_readwrite")
    
    if not os.path.exists("./log/running"):
        os.makedirs("./log/running")

if __name__ == "__main__":
    # mk_dirs()
    # storage, storage_init = execute_init()
    
    # storage_modified = {
    #     "init":storage_init
    # }
    # opcodes = load_opcodes("./data/game.disassemble")

    # for tx in load_data():
    #     if tx.get("tx_hash") == "0x8b20e7edcdb9a58a9d7b5fe08795ba0ff11bb8b4e0e1ebffeba03e2e50075681":
    #         verbose = True
    #     else:
    #         verbose = False
    #     storage, storage_read_write = execute_tx(
    #         storage=storage,
    #         transaction=tx,
    #         opcodes=opcodes,
    #         verbose=verbose
    #     )
    #     storage_modified[tx.get("tx_hash")] = storage_read_write
       
    # with open("result.json","w",encoding="utf-8") as f:
    #     json.dump(storage_modified,f,indent='\t')
    
    with open("result.json","r",encoding="utf-8") as f:
        storage_modified = json.load(f)
    
    group = load_group()
    commons = {}
    id_list = list(group.keys())
    for groupid in id_list:
        common_slots = check_common_slot(groupid,group[groupid],storage_modified)
        commons[groupid] = common_slots

    for i in range(0,len(id_list)):
        gameid = id_list[i]
        for j in range(i+1,len(id_list)):
            o_gameid = id_list[j]

            commons[gameid] = commons[gameid] - commons[o_gameid]
        commons[gameid] = list(commons[gameid])

    with open("commons.json","w",encoding="utf-8") as f:
        json.dump(commons,f,indent='\t')
    print()