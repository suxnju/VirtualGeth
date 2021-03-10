class EVM_stack:
	def __init__(self,stack:List[int]):
		self.stack = stack
	
	def __len__(self) -> int:
		return len(self.stack)

	# def __str__(self) -> str:
	# 	return "\n".join([
	# 			hex(v).strip("0x").rjust(64,"0")
	# 			for v in self.stack
	# 		]
	# 	)

	def __str__(self) -> str:
		return ",".join([
			hex(v) for v in self.stack
		])

	def _top_bytes(self,read_cnt:int=1) -> List[int]:
		assert len(self.stack) >= read_cnt

		if read_cnt == 1:
			return self.stack[0]
		return self.stack[:read_cnt]

	def _pop_bytes(self,read_cnt:int=1) -> List[int]:
		assert len(self.stack) >= read_cnt

		top_bytes = self.stack[:read_cnt]
		self.stack = self.stack[read_cnt:]

		if read_cnt == 1:
			return top_bytes[0]
		return top_bytes

	def _push_byte(self,value:int):
		self.stack = [value] + self.stack

	def _swap_byte(self,s_index=0,e_index=1):
		assert len(self.stack) > e_index

		tmp = self.stack[s_index]
		self.stack[e_index] = self.stack[s_index]
		self.stack[s_index] = tmp