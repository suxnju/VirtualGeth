class EVM_memory:
	def __init__(self,memory:Dict):
		self.memory = memory
	
	def __str__(self):
		return ",".join([
			hex(self.memory[i]) for i in range(10) if i in self.memory.keys()
			]
		)

	def set_value(self,offset:int,value:int):
		assert offset % 32 == 0

		self.memory[offset//32] = value

	def get(self,offset:int) -> int:
		assert offset % 32 == 0

		return self.memory[offset//32]

	def getConcat(self,offset:int,length:int) -> str:
		assert offset % 32 == 0
		bytes_count = length // 32
		
		result = ""
		for i in range(offset//32,offset//32+bytes_count):
			result += hex(self.memory[i]).strip("0x").rjust(64,"0")
		
		return result