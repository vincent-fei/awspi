description
=====
awspi(AWS Pi)社区版AWS运维开发小工具集  
由“DevOps on AWS”部分成员合作开发  
*还没弄好，请先别关注*

**功能列表：**  
ec2:创建，开启，关闭，删除，配置修改  
rds:  
s3:  
vpc:  
route53:  

**使用接口：**  
1，命令行工具：  
awspi [ec2|rds|s3] [function(create|start|stop)] [各自功能需要的参数]  
eg awspi ec2 start test1            #可以对test1操作进行开启  
2，webUI  

**用户安装配置：**  
1，rpm包提供（备选）。  
2，git仓库直接下载（备选）。  
3，python模块（备选）  

**实现方式：**  
1，封装一个awspi模块，提供功能列表所述方法，作为最原始的功能提供逻辑。  
awspi.type.function(arg1,arg2,arg3)  
eg: awspi.ec2.start(test1)  
2，利用成熟http框架（eg，django）输出http api，供外部程序调用 。  
3，编写命令行工具或者web工具，调用awspi http api实现aws操作。  

**产品形态：**  
C/S 或者 B/S  
S: 用来输出awspi api的http服务器  
C/B:  利用awspi api编写的客户程序  
