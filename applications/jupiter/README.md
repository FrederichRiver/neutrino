# Jupiter
Jupiter是一个工具包。它包含了最基础的功能：
1. 网络功能：network
2. 任务管理功能：task manager
3. 数据库管理功能：database manager
4. 基本函数：utils
5. 交易日模型：trade date
---
Network模块  
该模块实现3项功能：  
1. Random Header：用于生成随机的Http header。这个模块将来会改名字。  
2. fetch_html_object：用于从Html对象中获得一个etree模型，用于后续的内容分析。  
3. delay：一个简单的延时功能。  
---
Message Manager模块
该模块用于向各类终端发送信息。
