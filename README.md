# pyspider-stock

**Note:This README will have both Chinese and English version, Chinese first because it is for Chinese stock market.**

*Update* :

- [x] 增加[IT][1]版块股票的抓取和分析


## 这个项目做什么？
这个项目使用[pyspider][2]抓取[东方财富网股吧][3]、[雪球网][4]、[新浪股吧][5]的帖子，然后使用自然语言处理（情感分析）的方式分析舆论

所以

它有两个部分

1. 抓取帖子
2. 情感分析

## 如何运行它？

### 第一步 抓取帖子

* 下载[pyspider][6]，[mongoDB][7]，[redis][8]，[snowNLP][9]及相应的依赖库
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

如果想用[app][10]在android端查看结果，就保留

    os.system('mv data/' + grab_time + 'result.xls' + ' /var/www/html')


*English version*

## What's the aim of this project？
This project use [pyspider][11] to get posts of  [eastmoney][12], [xueqiu][13], [sinaguba][14],then use NLP techs to analyze the sentiment of public in order to select stocks.

SO

It has two parts

1. crawl posts
2. sentiment analysis

## How to run this project？

### Step 1 Crawl posts

* Download [pyspider][15]，[mongoDB][16]，[redis][17]，[snowNLP][18] and other dependencies
* run `set_hs300/setCodes.py`（in order to get all symbols of HS300 and load them into mongoDB）
* put `resultdb.py` into `database/mongodb` directory of **pyspider**（in order to save the crawling data to mongoDB）
* start `redis`
* **command line**  run `pyspider -c config.json all &` under directory of `config.json`
* copy script in `script` folder, paste code to your own project in localhost:5000, save
* click run button in localhost:5000

Complete two last steps before the market is open, then you'll get sentiment data everyday periodically.

### Step 2 Sentiment analysis

Run `main.py` after the posts been crawled and stored, also remember to create `data` directory for the first running.


## What happened？

Because of the stability, use `gubaEast.py` to crawl **GuYouHui** section is by default.

After Step 1 finished，you'll find a collection named `[date]GuYouHui` under a database called `[stockcode]eastmoney`, where `[stockcode]` and `[date]`are symbols of HS300 and date of yesterday.

Another part is sentiment analysis

The core part is three pieces of code：

    produceFactor.getSentimentFactor(stockCode, grab_time)
To obtain sentiment values and sentiment factor for a specific symbol **post** and crawl date（sentiment values are computed by snowNLP while sentiment factor is sentiment values times read numbers）

    aggregateFactor.aggregate(stockCode, grab_time)
To obtain sentiment values and sentiment factor for a specific symbol and crawl date（by adding all the posts for that stock on that day）, result is in `[date]SentimentFactor` under `[stockcode]eastmoney`

    dailyResult.setDailyResult(stockCode, grab_time)
To collect all the sentiment factors and number of posts for the crawl date,result is in the `DailyResult` collection which is under the `[date]`database.

Then an excel would be saved under the `data` directory as the final result.

The result would be mailed to specific users, through `sendMail` module.

Tasks under `taskdb` would be deleted in order to crawl posts periodically. Meanwhile data which stored 5 days ago would be dumped as backup and mongoDB would delete the original one. 

If you want to use the [app][19] to check the result on android, keep the following code 

    os.system('mv data/' + grab_time + 'result.xls' + ' /var/www/html')


  [1]: http://quote.eastmoney.com/center/list.html#28002737_0_2
  [2]: http://docs.pyspider.org/en/latest/
  [3]: http://guba.eastmoney.com/
  [4]: https://xueqiu.com/
  [5]: http://guba.sina.com.cn/
  [6]: http://docs.pyspider.org/en/latest/
  [7]: https://www.mongodb.com/
  [8]: https://redis.io/
  [9]: https://github.com/isnowfy/snownlp
  [10]: https://github.com/ryh95/huaxiApp
  [11]: http://docs.pyspider.org/en/latest/
  [12]: http://guba.eastmoney.com/
  [13]: https://xueqiu.com/
  [14]: http://guba.sina.com.cn/
  [15]: http://docs.pyspider.org/en/latest/
  [16]: https://www.mongodb.com/
  [17]: https://redis.io/
  [18]: https://github.com/isnowfy/snownlp
  [19]: https://github.com/ryh95/huaxiApp
