# VirtualGeth

## 任务
- 设计一个**虚拟执行环境**，观察交易在虚拟环境下的执行动作
  - 交易：在链上记录的成功执行的交易
  - 执行动作：对storage的读和写

- 目前来看，找到了更简洁的解决策略，就是使用geth的API:debug.traceTransaction(txid)
> - https://ethereum.stackexchange.com/questions/4282/how-to-check-the-vm-trace-using-geth
> - 需要同步节点信息Fast-sync https://support.chainstack.com/hc/en-us/articles/900003400806-Tracing-Ethereum-transactions

## 具体步骤
- 阅读go-ethereum的源码，主要参考 https://github.com/ZtesoftCS/go-ethereum-code-analysis
- 修改go-ethereum的源码，从中提取出需要的部分

## 任务进度
- [rlp源码解析](./rpl源码解析.md)