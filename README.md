## 通过多种方式爬取考研帮APP-玫瑰初相遇板块  
该项目主要通过fiddler抓包软件对考研帮APP进行抓包操作，找到要爬取板块的api，通过模拟构造参数对该板块进行抓取  

上面共有四个文件夹：  
第一个文件夹common就是普通的爬虫操作；  
第二个文件夹ip_from_myself是自己先创建一个ip代理池，然后在爬虫文件中调用自己ip代理池中的ip，[构建自己的ip代理池](https://github.com/hfxjd9527/ip_proxy_pool)  
第三个文件夹ip_from_other是使用[崔神的ip代理池](https://github.com/Python3WebSpider/ProxyPool)  
第四个文件夹multiprocess是分别使用自己的ip代理池和崔神的ip代理池的多进程爬虫  
  
------
------
  
注：  
1.如果使用[崔神的ip代理池](https://github.com/Python3WebSpider/ProxyPool)，在执行代码之前，需要先开启ip_proxy  
开启方法：  
进入到ProxyPool目录，按住shift点鼠标右键，选择“在此处打开打开命令窗口”，然后输入：  
python run.py  
就可以执行爬虫文件了。  

2.如果使用自己创建的ip代理池  
在开始爬虫前，需要自己先创建一个自用ip代理池，执行ip_pool.py文件即可，要确保MySQL数据库可连接。    
ip_judge.py用来从数据库中抽取ip并判断代理能不能用，不能用则删除，能用则结束。    
在kyb.py中会调用ip_judge文件，它会一直执行ip_judge文件，直到有可用ip为自己所用。    

下面是要爬取的板块，嘻嘻  

![image](https://github.com/hfxjd9527/kaoyanbang/blob/master/kyb.gif)
