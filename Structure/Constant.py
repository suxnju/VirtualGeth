from .Transaction import Transaction

class Constant:
	MODULO = 2**256
	UPPER_UINT256 = 2**256 - 1

	msg_caller = Transaction.From
	msg_value = Transaction.Value
	timestamp = Transaction.Timestamp