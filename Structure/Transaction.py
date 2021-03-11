import time
import datetime

def get_timestamp(block_time,UTC=True):
	if UTC:
		dt = datetime.datetime.strptime(block_time, "%Y-%m-%d %H:%M:%S UTC") + datetime.timedelta(hours=8)
	else:
		dt = datetime.datetime.strptime(block_time, "%Y-%m-%d %H:%M:%S")
	timestamp = datetime.datetime.timestamp(dt)
	return int(timestamp)

def get_time(timestamp):
	time_local = time.localtime(timestamp)
	block_time = time.strftime("%Y-%m-%d %H:%M:%S UTC",time_local)
	return block_time

class Transaction:
	def __init__(self,tx_hash:str,msg_caller:str,msg_value:int,msg_input:str,timestamp:str):
		self.tx_hash = tx_hash
		self.msg_caller = int(msg_caller,16)
		self.msg_value = msg_value
		self.msg_input = int(msg_input,16)
		self.timestamp = get_timestamp(timestamp)

	def get(self,key):
		return self.__dict__[key]

if __name__ == "__main__":
	tx = Transaction(
		tx_hash="0xaa8fcdb649889f7f1b63c37f34902650ffb2faedea4b3c6b6630f251f8aedbd8",
		msg_caller="0x5dc12131e65b8f395ab11a2c4e6af717e1b179ba",
		msg_value=50000000000000000,
		msg_input="0xfe1f6a0bd579d4fe1e90a03d545e3d8c01dfc19c2ae3b26ad26ba994a1dec89a435a3dc00000000000000000000000000000000000000000000000000000000000000000",
		timestamp="2018-08-19 15:05:16 UTC"
	)
	
	print(tx.get("msg_caller"))