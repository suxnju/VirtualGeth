from typing import List,Dict
from .utils import keccak256

from Constant import Constant
from Stack import EVM_stack
from Memory import EVM_memory
from Storage import EVM_storage

class EVM:
	def __init__(self,Stack:EVM_stack,Memory:EVM_memory,Storage:EVM_storage):
		self.Stack = Stack
		self.Memory = Memory
		self.Storage = Storage

		self.pc = 0
		self.args = None

	def STOP(self):
		'''
			00 \\
			STOP() \\
			halts execution of the contract
		'''
		raise ValueError('Not implement STOP error!')

	def ADD(self):
		'''
			01 \\
			a+b \\
			(u)int256 addition modulo 2**256
		'''
		assert len(self.Stack) >= 2
		a,b = self.Stack._pop_bytes(2)
		c = a + b
		if c>Constant.MODULO:
			logging.warning("Integer overflow")
		c = c%Constant.MODULO
		
		self.Stack._push_byte(c)

	def MUL(self):
		'''
			02 \\
			a*b \\
			(u)int256 multiplication modulo 2**256
		'''
		assert len(self.Stack) >= 2
		a,b = self.Stack._pop_bytes(2)
		c = a * b
		c = c%Constant.MODULO
		
		self.Stack._push_byte(c)

	def SUB(self):
		'''
			03 \\
			a-b \\
			(u)int256 subtraction modulo 2**256
		'''
		assert len(self.Stack) >= 2
		a,b = self.Stack._pop_bytes(2)
		c = a - b
		c = c%Constant.MODULO
		
		self.Stack._push_byte(c)

	def DIV(self):
		'''
			04 \\
			a//b \\
			uint256 division
		'''
		assert len(self.Stack) >= 2
		a,b = self.Stack._pop_bytes(2)
		c = a / b
		if c>Constant.MODULO:
			logging.warning("Integer overflow")
		c = c%Constant.MODULO
		
		self.Stack._push_byte(c)

	def SDIV(self):
		'''
			05 \\
			a//b \\
			int256 division
		'''
		raise ValueError('Not implement SDIV error!')

	def MOD(self):
		'''
			06 \\
			a%b \\
			uint256 modulus
		'''
		raise ValueError('Not implement MOD error!')

	def SMOD(self):
		'''
			07 \\
			a%b \\
			int256 modulus
		'''
		raise ValueError('Not implement SMOD error!')

	def ADDMOD(self):
		'''
			08 \\
			(a+b)%N \\
			(u)int256 addition modulo N
		'''
		raise ValueError('Not implement ADDMOD error!')

	def MULMOD(self):
		'''
			09 \\
			(a*b)%N \\
			(u)int256 multiplication modulo N
		'''
		raise ValueError('Not implement MULMOD error!')

	def EXP(self):
		'''
			0A \\
			a**b \\
			uint256 exponentiation modulo 2**256
		'''
		assert len(self.Stack) >= 2
		a,b = self.Stack._pop_bytes(2)
		c = a ** b
		c = c%Constant.MODULO
		
		self.Stack._push_byte(c)

	def SIGNEXTEND(self):
		'''
			0B \\
			y=SIGNEXTEND(x,b) \\
			sign extends x from (b + 1) * 8 bits to 256 bits.
		'''
		b,x = self.Stack._pop_bytes(2)
		pos = 8 * (b + 1)
		sign_bit = (1 << pos-1)
		if x & sign_bit:
			y = x | (UPPER - sign_bit)
		else:
			y = x & (sign_bit - 1)
		self.Stack._push_byte(y)

	def LT(self):
		'''
			10 \\
			a<b \\
			uint256 comparison
		'''
		raise ValueError('Not implement LT error!')

	def GT(self):
		'''
			11 \\
			a>b \\
			uint256 comparison
		'''
		raise ValueError('Not implement GT error!')

	def SLT(self):
		'''
			12 \\
			a<b \\
			int256 comparison
		'''
		raise ValueError('Not implement SLT error!')

	def SGT(self):
		'''
			13 \\
			a>b \\
			int256 comparison
		'''
		raise ValueError('Not implement SGT error!')

	def EQ(self):
		'''
			14 \\
			a==b \\
			(u)int256 equality
		'''
		raise ValueError('Not implement EQ error!')

	def ISZERO(self):
		'''
			15 \\
			a==0 \\
			(u)int256 is zero
		'''
		raise ValueError('Not implement ISZERO error!')

	def AND(self):
		'''
			16 \\
			a&b \\
			256-bit bitwise and
		'''
		a,b = self.Stack._pop_bytes(2)
		self.Stack._push_byte(a&b)

	def OR(self):
		'''
			17 \\
			a|b \\
			256-bit bitwise or
		'''
		a,b = self.Stack._pop_bytes(2)
		self.Stack._push_byte(a|b)

	def XOR(self):
		'''
			18 \\
			a^b \\
			256-bit bitwise xor
		'''
		raise ValueError('Not implement XOR error!')

	def NOT(self):
		'''
			19 \\
			~a \\
			256-bit bitwise not
		'''
		a = self.Stack._pop_bytes()
		self.Stack._push_byte(~a)

	def BYTE(self):
		'''
			1A \\
			y=(x>>(248-i*8))&0xFF \\
			ith byte of (u)int256 x, counting from most significant byte
		'''
		raise ValueError('Not implement BYTE error!')

	def SHL(self):
		'''
			1B \\
			value<<shift \\
			256-bit shift left
		'''
		raise ValueError('Not implement SHL error!')

	def SHR(self):
		'''
			1C \\
			value>>shift \\
			256-bit shift right
		'''
		raise ValueError('Not implement SHR error!')

	def SAR(self):
		'''
			1D \\
			value>>shift \\
			int256 shift right
		'''
		raise ValueError('Not implement SAR error!')

	def SHA3(self):
		'''
			20 \\
			hash=keccak256(memory[offset:offset+length]) \\
			keccak256
		'''
		offset,length = self.Stack._pop_bytes(2)
		to_hash = self.Memory.getConcat(offset,length)
		value = int(keccak256(to_hash,is_hex=True),16)
		self.Stack._push_byte(value)

	def ADDRESS(self):
		'''
			30 \\
			address(this) \\
			address of the executing contract
		'''
		raise ValueError('Not implement ADDRESS error!')

	def BALANCE(self):
		'''
			31 \\
			address(addr).balance \\
			address balance in wei
		'''
		raise ValueError('Not implement BALANCE error!')

	def ORIGIN(self):
		'''
			32 \\
			tx.origin \\
			transaction origin address
		'''
		raise ValueError('Not implement ORIGIN error!')

	def CALLER(self):
		'''
			33 \\
			msg.caller \\
			message caller address
		'''
		self.Stack._push_byte(Constant.msg_caller)

	def CALLVALUE(self):
		'''
			34 \\
			msg.value \\
			message funds in wei
		'''
		self.Stack._push_byte(Constant.msg_value)

	def CALLDATALOAD(self):
		'''
			35 \\
			msg.data[i:i+32] \\
			reads a (u)int256 from message data
		'''
		raise ValueError('Not implement CALLDATALOAD error!')

	def CALLDATASIZE(self):
		'''
			36 \\
			msg.data.size \\
			message data length in bytes
		'''
		raise ValueError('Not implement CALLDATASIZE error!')

	def CALLDATACOPY(self):
		'''
			37 \\
			memory[destOffset:destOffset+length]=msg.data[offset:offset+length] \\
			copy message data
		'''
		raise ValueError('Not implement CALLDATACOPY error!')

	def CODESIZE(self):
		'''
			38 \\
			address(this).code.size \\
			length of the executing contract's code in bytes
		'''
		raise ValueError('Not implement CODESIZE error!')

	def CODECOPY(self):
		'''
			39 \\
			memory[destOffset:destOffset+length]=address(this).code[offset:offset+length] \\
			copy executing contract's bytecode
		'''
		raise ValueError('Not implement CODECOPY error!')

	def GASPRICE(self):
		'''
			3A \\
			tx.gasprice \\
			gas price of the executing transaction, in wei per unit of gas
		'''
		raise ValueError('Not implement GASPRICE error!')

	def EXTCODESIZE(self):
		'''
			3B \\
			address(addr).code.size \\
			length of the contract bytecode at addr, in bytes
		'''
		raise ValueError('Not implement EXTCODESIZE error!')

	def EXTCODECOPY(self):
		'''
			3C \\
			memory[destOffset:destOffset+length]=address(addr).code[offset:offset+length] \\
			copy contract's bytecode
		'''
		raise ValueError('Not implement EXTCODECOPY error!')

	def RETURNDATASIZE(self):
		'''
			3D \\
			size=RETURNDATASIZE() \\
			the size of the returned data from the last external call, in bytes
		'''
		raise ValueError('Not implement RETURNDATASIZE error!')

	def RETURNDATACOPY(self):
		'''
			3E \\
			memory[destOffset:destOffset+length]=RETURNDATA[offset:offset+length] \\
			copy returned data
		'''
		raise ValueError('Not implement RETURNDATACOPY error!')

	def EXTCODEHASH(self):
		'''
			3F \\
			hash=address(addr).exists?keccak256(address(addr).code):0 \\
			hash of the contract bytecode at addr, see EIP-1052
		'''
		raise ValueError('Not implement EXTCODEHASH error!')

	def BLOCKHASH(self):
		'''
			40 \\
			hash=block.blockHash(blockNumber) \\
			hash of the specific block, only valid for the 256 most recent blocks, excluding the current one
		'''
		raise ValueError('Not implement BLOCKHASH error!')

	def COINBASE(self):
		'''
			41 \\
			block.coinbase \\
			address of the current block's miner
		'''
		raise ValueError('Not implement COINBASE error!')

	def TIMESTAMP(self):
		'''
			42 \\
			block.timestamp \\
			current block's Unix timestamp in seconds
		'''
		self.Stack._push_byte(Constant.timestamp)

	def NUMBER(self):
		'''
			43 \\
			block.number \\
			current block's number
		'''
		raise ValueError('Not implement NUMBER error!')

	def DIFFICULTY(self):
		'''
			44 \\
			block.difficulty \\
			current block's difficulty
		'''
		raise ValueError('Not implement DIFFICULTY error!')

	def GASLIMIT(self):
		'''
			45 \\
			block.gaslimit \\
			current block's gas limit
		'''
		raise ValueError('Not implement GASLIMIT error!')

	def POP(self):
		'''
			50 \\
			POP() \\
			pops a (u)int256 off the stack and discards it
		'''
		self.Stack._pop_bytes()

	def MLOAD(self):
		'''
			51 \\
			value=memory[offset:offset+32] \\
			reads a (u)int256 from memory
		'''
		offset = self.Stack._pop_bytes()
		value = self.Memory.get(offset)
		self.Stack._push_byte(value)

	def MSTORE(self):
		'''
			52 \\
			memory[offset:offset+32]=value \\
			writes a (u)int256 to memory
		'''
		offset,value = self.Stack._pop_bytes(2)
		self.Memory.set_value(offset,value)

	def MSTORE8(self):
		'''
			53 \\
			memory[offset]=value&0xFF \\
			writes a uint8 to memory
		'''
		raise ValueError('Not implement MSTORE8 error!')

	def SLOAD(self):
		'''
			54 \\
			value=storage[key] \\
			reads a (u)int256 from storage
		'''
		key = self.Stack._pop_bytes()
		value = self.Storage.get(key)
		self.Stack._push_byte(value)

	def SSTORE(self):
		'''
			55 \\
			storage[key]=value \\
			writes a (u)int256 to storage
		'''
		key,value = self.Stack._pop_bytes(2)
		self.Storage.set_key(key,value)

	def JUMP(self):
		'''
			56 \\
			$pc=destination \\
			unconditional jump
		'''
		raise ValueError('Not implement JUMP error!')

	def JUMPI(self):
		'''
			57 \\
			$pc=cond?destination:$pc+1 \\
			conditional jump if condition is truthy
		'''
		raise ValueError('Not implement JUMPI error!')

	def PC(self):
		'''
			58 \\
			$pc \\
			program counter
		'''
		raise ValueError('Not implement PC error!')

	def MSIZE(self):
		'''
			59 \\
			size=MSIZE() \\
			size of memory for this contract execution, in bytes
		'''
		raise ValueError('Not implement MSIZE error!')

	def GAS(self):
		'''
			5A \\
			gasRemaining=GAS() \\
			remaining gas
		'''
		raise ValueError('Not implement GAS error!')

	def JUMPDEST(self):
		'''
			5B \\
			\\
			metadata to annotate possible jump destinations
		'''
		pass

	def PUSH1(self):
		'''
			60 \\
			PUSH(uint8) \\
			pushes a 1-byte value onto the stack
		'''
		self.Stack._push_byte(self.args)

	def PUSH2(self):
		'''
			61 \\
			PUSH(uint16) \\
			pushes a 2-byte value onto the stack
		'''
		self.Stack._push_byte(self.args)

	def PUSH3(self):
		'''
			62 \\
			PUSH(uint24) \\
			pushes a 3-byte value onto the stack
		'''
		self.Stack._push_byte(self.args)

	def PUSH4(self):
		'''
			63 \\
			PUSH(uint32) \\
			pushes a 4-byte value onto the stack
		'''
		self.Stack._push_byte(self.args)

	def PUSH5(self):
		'''
			64 \\
			PUSH(uint40) \\
			pushes a 5-byte value onto the stack
		'''
		self.Stack._push_byte(self.args)

	def PUSH6(self):
		'''
			65 \\
			PUSH(uint48) \\
			pushes a 6-byte value onto the stack
		'''
		self.Stack._push_byte(self.args)

	def PUSH7(self):
		'''
			66 \\
			PUSH(uint56) \\
			pushes a 7-byte value onto the stack
		'''
		self.Stack._push_byte(self.args)

	def PUSH8(self):
		'''
			67 \\
			PUSH(uint64) \\
			pushes a 8-byte value onto the stack
		'''
		self.Stack._push_byte(self.args)

	def PUSH9(self):
		'''
			68 \\
			PUSH(uint72) \\
			pushes a 9-byte value onto the stack
		'''
		self.Stack._push_byte(self.args)

	def PUSH10(self):
		'''
			69 \\
			PUSH(uint80) \\
			pushes a 10-byte value onto the stack
		'''
		self.Stack._push_byte(self.args)

	def PUSH11(self):
		'''
			6A \\
			PUSH(uint88) \\
			pushes a 11-byte value onto the stack
		'''
		self.Stack._push_byte(self.args)

	def PUSH12(self):
		'''
			6B \\
			PUSH(uint96) \\
			pushes a 12-byte value onto the stack
		'''
		self.Stack._push_byte(self.args)

	def PUSH13(self):
		'''
			6C \\
			PUSH(uint104) \\
			pushes a 13-byte value onto the stack
		'''
		self.Stack._push_byte(self.args)

	def PUSH14(self):
		'''
			6D \\
			PUSH(uint112) \\
			pushes a 14-byte value onto the stack
		'''
		self.Stack._push_byte(self.args)

	def PUSH15(self):
		'''
			6E \\
			PUSH(uint120) \\
			pushes a 15-byte value onto the stack
		'''
		self.Stack._push_byte(self.args)

	def PUSH16(self):
		'''
			6F \\
			PUSH(uint128) \\
			pushes a 16-byte value onto the stack
		'''
		self.Stack._push_byte(self.args)

	def PUSH17(self):
		'''
			70 \\
			PUSH(uint136) \\
			pushes a 17-byte value onto the stack
		'''
		self.Stack._push_byte(self.args)

	def PUSH18(self):
		'''
			71 \\
			PUSH(uint144) \\
			pushes a 18-byte value onto the stack
		'''
		self.Stack._push_byte(self.args)

	def PUSH19(self):
		'''
			72 \\
			PUSH(uint152) \\
			pushes a 19-byte value onto the stack
		'''
		self.Stack._push_byte(self.args)

	def PUSH20(self):
		'''
			73 \\
			PUSH(uint160) \\
			pushes a 20-byte value onto the stack
		'''
		self.Stack._push_byte(self.args)

	def PUSH21(self):
		'''
			74 \\
			PUSH(uint168) \\
			pushes a 21-byte value onto the stack
		'''
		self.Stack._push_byte(self.args)

	def PUSH22(self):
		'''
			75 \\
			PUSH(uint176) \\
			pushes a 22-byte value onto the stack
		'''
		self.Stack._push_byte(self.args)

	def PUSH23(self):
		'''
			76 \\
			PUSH(uint184) \\
			pushes a 23-byte value onto the stack
		'''
		self.Stack._push_byte(self.args)

	def PUSH24(self):
		'''
			77 \\
			PUSH(uint192) \\
			pushes a 24-byte value onto the stack
		'''
		self.Stack._push_byte(self.args)

	def PUSH25(self):
		'''
			78 \\
			PUSH(uint200) \\
			pushes a 25-byte value onto the stack
		'''
		self.Stack._push_byte(self.args)

	def PUSH26(self):
		'''
			79 \\
			PUSH(uint208) \\
			pushes a 26-byte value onto the stack
		'''
		self.Stack._push_byte(self.args)

	def PUSH27(self):
		'''
			7A \\
			PUSH(uint216) \\
			pushes a 27-byte value onto the stack
		'''
		self.Stack._push_byte(self.args)

	def PUSH28(self):
		'''
			7B \\
			PUSH(uint224) \\
			pushes a 28-byte value onto the stack
		'''
		self.Stack._push_byte(self.args)

	def PUSH29(self):
		'''
			7C \\
			PUSH(uint232) \\
			pushes a 29-byte value onto the stack
		'''
		self.Stack._push_byte(self.args)

	def PUSH30(self):
		'''
			7D \\
			PUSH(uint240) \\
			pushes a 30-byte value onto the stack
		'''
		self.Stack._push_byte(self.args)

	def PUSH31(self):
		'''
			7E \\
			PUSH(uint248) \\
			pushes a 31-byte value onto the stack
		'''
		self.Stack._push_byte(self.args)

	def PUSH32(self):
		'''
			7F \\
			PUSH(uint256) \\
			pushes a 32-byte value onto the stack
		'''
		self.Stack._push_byte(self.args)

	def DUP1(self):
		'''
			80 \\
			PUSH(value) \\
			clones the last value on the stack
		'''
		value = self.Stack._top_bytes(read_cnt=1)
		self.Stack._push_byte(value)

	def DUP2(self):
		'''
			81 \\
			PUSH(value) \\
			clones the 2nd last value on the stack
		'''
		value = self.Stack._top_bytes(read_cnt=2)[-1]
		self.Stack._push_byte(value)

	def DUP3(self):
		'''
			82 \\
			PUSH(value) \\
			clones the 3rd last value on the stack
		'''
		value = self.Stack._top_bytes(read_cnt=3)[-1]
		self.Stack._push_byte(value)

	def DUP4(self):
		'''
			83 \\
			PUSH(value) \\
			clones the 4th last value on the stack
		'''
		value = self.Stack._top_bytes(read_cnt=4)[-1]
		self.Stack._push_byte(value)

	def DUP5(self):
		'''
			84 \\
			PUSH(value) \\
			clones the 5th last value on the stack
		'''
		value = self.Stack._top_bytes(read_cnt=5)[-1]
		self.Stack._push_byte(value)

	def DUP6(self):
		'''
			85 \\
			PUSH(value) \\
			clones the 6th last value on the stack
		'''
		value = self.Stack._top_bytes(read_cnt=6)[-1]
		self.Stack._push_byte(value)

	def DUP7(self):
		'''
			86 \\
			PUSH(value) \\
			clones the 7th last value on the stack
		'''
		value = self.Stack._top_bytes(read_cnt=7)[-1]
		self.Stack._push_byte(value)

	def DUP8(self):
		'''
			87 \\
			PUSH(value) \\
			clones the 8th last value on the stack
		'''
		value = self.Stack._top_bytes(read_cnt=8)[-1]
		self.Stack._push_byte(value)

	def DUP9(self):
		'''
			88 \\
			PUSH(value) \\
			clones the 9th last value on the stack
		'''
		value = self.Stack._top_bytes(read_cnt=9)[-1]
		self.Stack._push_byte(value)

	def DUP10(self):
		'''
			89 \\
			PUSH(value) \\
			clones the 10th last value on the stack
		'''
		value = self.Stack._top_bytes(read_cnt=10)[-1]
		self.Stack._push_byte(value)

	def DUP11(self):
		'''
			8A \\
			PUSH(value) \\
			clones the 11th last value on the stack
		'''
		value = self.Stack._top_bytes(read_cnt=11)[-1]
		self.Stack._push_byte(value)

	def DUP12(self):
		'''
			8B \\
			PUSH(value) \\
			clones the 12th last value on the stack
		'''
		value = self.Stack._top_bytes(read_cnt=12)[-1]
		self.Stack._push_byte(value)

	def DUP13(self):
		'''
			8C \\
			PUSH(value) \\
			clones the 13th last value on the stack
		'''
		value = self.Stack._top_bytes(read_cnt=13)[-1]
		self.Stack._push_byte(value)

	def DUP14(self):
		'''
			8D \\
			PUSH(value) \\
			clones the 14th last value on the stack
		'''
		value = self.Stack._top_bytes(read_cnt=14)[-1]
		self.Stack._push_byte(value)

	def DUP15(self):
		'''
			8E \\
			PUSH(value) \\
			clones the 15th last value on the stack
		'''
		value = self.Stack._top_bytes(read_cnt=15)[-1]
		self.Stack._push_byte(value)
	
	def DUP16(self):
		'''
			8F \\
			PUSH(value) \\
			clones the 16th last value on the stack
		'''
		value = self.Stack._top_bytes(read_cnt=16)[-1]
		self.Stack._push_byte(value)

	def SWAP1(self):
		'''
			90 \\
			a,b=b,a \\
			swaps the last two values on the stack
		'''
		self.Stack._swap_byte(e_index=1)

	def SWAP2(self):
		'''
			91 \\
			a,b=b,a \\
			swaps the top of the stack with the 3rd last element
		'''
		self.Stack._swap_byte(e_index=2)

	def SWAP3(self):
		'''
			92 \\
			a,b=b,a \\
			swaps the top of the stack with the 4th last element
		'''
		self.Stack._swap_byte(e_index=3)

	def SWAP4(self):
		'''
			93 \\
			a,b=b,a \\
			swaps the top of the stack with the 5th last element
		'''
		self.Stack._swap_byte(e_index=4)

	def SWAP5(self):
		'''
			94 \\
			a,b=b,a \\
			swaps the top of the stack with the 6th last element
		'''
		self.Stack._swap_byte(e_index=5)

	def SWAP6(self):
		'''
			95 \\
			a,b=b,a \\
			swaps the top of the stack with the 7th last element
		'''
		self.Stack._swap_byte(e_index=6)

	def SWAP7(self):
		'''
			96 \\
			a,b=b,a \\
			swaps the top of the stack with the 8th last element
		'''
		self.Stack._swap_byte(e_index=7)

	def SWAP8(self):
		'''
			97 \\
			a,b=b,a \\
			swaps the top of the stack with the 9th last element
		'''
		self.Stack._swap_byte(e_index=8)

	def SWAP9(self):
		'''
			98 \\
			a,b=b,a \\
			swaps the top of the stack with the 10th last element
		'''
		self.Stack._swap_byte(e_index=9)

	def SWAP10(self):
		'''
			99 \\
			a,b=b,a \\
			swaps the top of the stack with the 11th last element
		'''
		self.Stack._swap_byte(e_index=10)

	def SWAP11(self):
		'''
			9A \\
			a,b=b,a \\
			swaps the top of the stack with the 12th last element
		'''
		self.Stack._swap_byte(e_index=11)

	def SWAP12(self):
		'''
			9B \\
			a,b=b,a \\
			swaps the top of the stack with the 13th last element
		'''
		self.Stack._swap_byte(e_index=12)

	def SWAP13(self):
		'''
			9C \\
			a,b=b,a \\
			swaps the top of the stack with the 14th last element
		'''
		self.Stack._swap_byte(e_index=13)

	def SWAP14(self):
		'''
			9D \\
			a,b=b,a \\
			swaps the top of the stack with the 15th last element
		'''
		self.Stack._swap_byte(e_index=14)

	def SWAP15(self):
		'''
			9E \\
			a,b=b,a \\
			swaps the top of the stack with the 16th last element
		'''
		self.Stack._swap_byte(e_index=15)

	def SWAP16(self):
		'''
			9F \\
			a,b=b,a \\
			swaps the top of the stack with the 17th last element
		'''
		self.Stack._swap_byte(e_index=16)

	def LOG0(self):
		'''
			A0 \\
			LOG0(memory[offset:offset+length]) \\
			fires an event
		'''
		raise ValueError('Not implement LOG0 error!')

	def LOG1(self):
		'''
			A1 \\
			LOG1(memory[offset:offset+length],topic0) \\
			fires an event
		'''
		raise ValueError('Not implement LOG1 error!')

	def LOG2(self):
		'''
			A2 \\
			LOG2(memory[offset:offset+length],topic0,topic1) \\
			fires an event
		'''
		raise ValueError('Not implement LOG2 error!')

	def LOG3(self):
		'''
			A3 \\
			LOG3(memory[offset:offset+length],topic0,topic1,topic2) \\
			fires an event
		'''
		raise ValueError('Not implement LOG3 error!')

	def LOG4(self):
		'''
			A4 \\
			LOG4(memory[offset:offset+length],topic0,topic1,topic2,topic3) \\
			fires an event
		'''
		raise ValueError('Not implement LOG4 error!')

	def PUSH(self):
		'''
			B0 \\
			??? \\
			???
		'''
		raise ValueError('Not implement PUSH error!')

	def DUP(self):
		'''
			B1 \\
			??? \\
			???
		'''
		raise ValueError('Not implement DUP error!')

	def SWAP(self):
		'''
			B2 \\
			??? \\
			???
		'''
		raise ValueError('Not implement SWAP error!')

	def CREATE(self):
		'''
			F0 \\
			addr=newmemory[offset:offset+length].value(value) \\
			creates a child contract
		'''
		raise ValueError('Not implement CREATE error!')

	def CALL(self):
		'''
			F1 \\
			success,memory[retOffset:retOffset+retLength]=address(addr).call.gas(gas).value(value)(memory[argsOffset:argsOffset+argsLength]) \\
			calls a method in another contract
		'''
		raise ValueError('Not implement CALL error!')

	def CALLCODE(self):
		'''
			F2 \\
			success,memory[retOffset:retOffset+retLength]=address(addr).callcode.gas(gas).value(value)(memory[argsOffset:argsOffset+argsLength]) \\
			???
		'''
		raise ValueError('Not implement CALLCODE error!')

	def RETURN(self):
		'''
			F3 \\
			returnmemory[offset:offset+length] \\
			returns from this contract call
		'''
		raise ValueError('Not implement RETURN error!')

	def DELEGATECALL(self):
		'''
			F4 \\
			success,memory[retOffset:retOffset+retLength]=address(addr).delegatecall.gas(gas)(memory[argsOffset:argsOffset+argsLength]) \\
			calls a method in another contract, using the storage of the current contract
		'''
		raise ValueError('Not implement DELEGATECALL error!')

	def CREATE2(self):
		'''
			F5 \\
			addr=newmemory[offset:offset+length].value(value) \\
			creates a child contract with a deterministic address, see EIP-1014
		'''
		raise ValueError('Not implement CREATE2 error!')

	def STATICCALL(self):
		'''
			FA \\
			success,memory[retOffset:retOffset+retLength]=address(addr).staticcall.gas(gas)(memory[argsOffset:argsOffset+argsLength]) \\
			calls a method in another contract with state changes such as contract creation, event emission, storage modification and contract destruction disallowed, see EIP-214
		'''
		raise ValueError('Not implement STATICCALL error!')

	def REVERT(self):
		'''
			FD \\
			revert(memory[offset:offset+length]) \\
			reverts with return data
		'''
		raise ValueError('Not implement REVERT error!')

	def SELFDESTRUCT(self):
		'''
			FF \\
			selfdestruct(address(addr)) \\
			destroys the contract and sends all funds to addr.
		'''
		raise ValueError('Not implement SELFDESTRUCT error!')




if __name__ == "__main__":
	evm = EVM(
		EVM_stack([1,2,3]),
		EVM_memory([]),
		EVM_storage({})
	)

	evm.ADD()

	print(str(evm.Stack))