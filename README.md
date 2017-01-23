# pyspider-stock

## 这个项目做什么？
这个项目使用[pyspider][1]抓取[东方财富网股吧][2]、[雪球网][3]、[新浪股吧][4]的帖子，然后使用自然语言处理（情感分析）的方式分析舆论

所以

它有两个部分

1. 抓取帖子
2. 情感分析

## 如何运行它？

### 第一步 抓取帖子

* 下载[pyspider][5]，[mongoDB][6]，[redis][7]，[snowNLP][8]及相应的依赖库
* 运行`set_hs300/setCodes.py`（为了将HS300成份股的股票代码装入mongoDB）
* 然后，将`resultdb.py`放入pyspider的`database/mongodb`目录下（为了将爬取到的数据放入mongoDB）
* 启动`redis`
* 然后，在有`config.json`的目录下，**command line** 运行`pyspider -c config.json all &`
* 其次，将script里的脚本复制后，粘贴到localhost：5000下你自己的工程里（想要爬取哪个网站就粘贴哪个script），保存
* 最后在网页localhost:5000里单击run

在早上开盘前执行完最后两步即可在每天早上开盘前获取到HS300昨日的舆论数据

### 第二步 情感分析
在完成第一步30分钟后即可执行该步骤
第一次运行时在和`main.py`同目录下新建目录`data`
运行 `main.py`即可


## 发生了什么？

默认使用`gubaEast.py`抓取东方财富网下的**股友汇**版块，因为它最稳定

执行完第一步后，你会在名为`[stockcode]eastmoney`的database下发现`[date]GuYouHui`的collection，其中`[stockcode]`和`[date]`分别是HS300成份股的股票代码和昨天的日期

接着是情感分析部分

核心是3段代码：

    produceFactor.getSentimentFactor(stockCode, grab_time)
用于获得抓取日期的特定股票帖子的情感因子和情感值（由情感因子乘以阅读量获得）

    aggregateFactor.aggregate(stockCode, grab_time)
用于获得抓取日期的特定股票的情感值（由所有帖子情感值相加得到），结果保存在`[stockcode]eastmoney`下的`[date]SentimentFactor`中

    dailyResult.setDailyResult(stockCode, grab_time)
用于汇总抓取日期的所有HS300股票的情感值和帖子数，结果在`[date]`database的`DailyResult`collection下

而后结果会以excel的格式保存在`data`目录下

结果会以邮件形式发给你指定的人，通过`sendMail`模块

最后taskdb里面这个任务会被清除，以便明天增量抓取。同时会将5天前数据库中的数据导出，存在本地，并删除数据库中的数据

如果想用[app][9]在android端查看结果，就保留

    os.system('mv data/' + grab_time + 'result.xls' + ' /var/www/html')


  [1]: http://docs.pyspider.org/en/latest/
  [2]: http://guba.eastmoney.com/
  [3]: https://xueqiu.com/
  [4]: http://guba.sina.com.cn/
  [5]: http://docs.pyspider.org/en/latest/
  [6]: https://www.mongodb.com/
  [7]: https://redis.io/
  [8]: https://github.com/isnowfy/snownlp
  [9]: https://github.com/ryh95/huaxiApp
