# VirtualGeth

## 任务
- 设计一个**虚拟执行环境**，观察交易在虚拟环境下的执行动作
  - 交易：在链上记录的成功执行的交易
  - 执行动作：对storage的读和写

- **目前来看，找到了更简洁的解决策略，就是使用geth的API:debug.traceTransaction(txid)**
  - https://ethereum.stackexchange.com/questions/4282/how-to-check-the-vm-trace-using-geth
  - **需要同步节点信息**Fast-sync https://support.chainstack.com/hc/en-us/articles/900003400806-Tracing-Ethereum-transactions
  - 执行速度慢