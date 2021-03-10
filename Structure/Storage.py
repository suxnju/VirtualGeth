

class EVM_storage:
	def __init__(self,storage:Dict):
		self.storage = storage

	def __str__(self):
		return ",".join(
			[
				hex(self.storage[i]) for i in range(12) if i in self.storage.keys()
			]
		)

	def get(self,key:int) -> int:
		# assert key in self.storage.keys()
		if key in self.storage.keys():
			return self.storage[key]
		else:
			return 0
	
	def set_key(self,key:int,value:int):
		self.storage[key] = value
