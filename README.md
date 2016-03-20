# pyspider-stock

1.这个项目运用pyspider爬取一些股票论坛网站

比如：

http://guba.sina.com.cn/

http://xueqiu.com/

http://guba.eastmoney.com/default,2,f_1.html

2.关于最外层script说明如下

2.1关于script的使用

首先，下载pyspider，mongoDB，redis，及相应的依赖库

其次，将最外面的script复制后，粘贴到localhost：5000下你自己的script里（想要爬取哪个网站就粘贴哪个script），保存

然后，将resultdb.py放入pyspider的database/mongodb目录下（覆盖原来的）

然后，在有config.json的目录下，command line 运行‘pyspider -c config.json all &’

大功告成，等待mongodb的数据吧

2.2关于script目前已经完成

目前东方财富网的script可以抓取任意股票的任意板块，可以自动更新（这对股票数据很关键）

雪球网和新浪股吧的还需要测试和扩充

2.3script将要做的

测试雪球和新浪的运行情况

3.关于east sentiment

east sentiment以某一个股票为例（601001）

分析舆论和股票价格的相关性

用到的工具有

snownlp numpy pandas matplotlib ...

4.关于set stockcodes 

这个是将沪深300的成分股的股票代码录入mongodb

用于方便处理数据
