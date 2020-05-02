
# 豆果美食APP 菜谱爬取

## 主要功能
爬取豆果美食APP菜谱分类中的菜谱数据，并存到mongodb

## 架构
1.whistle 分析数据包
2.夜神安卓模拟器 安装豆果app
3.python 编写爬虫代码
4.vscode 编辑器
5.mongodb 存储数据
6.ROBO 3T mongoDB可视化工具 

## 遇到的问题

Q:报错信息
> while queue_list.qsize() > 0:
  File "/Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/multiprocessing/queues.py", line 120, in qsize
    return self._maxsize - self._sem._semlock._get_value()
    
A:
mac os 中 queue.qsize() 报错。暂时的解决办法是，使用queue.empty 来解决
原代码：
```python
while queue_list.qsize() > 0:
  pool.submit(handle_search,queue_list.get()) # 函数 和参数
```
修改后：
```python
....
while not queue_list.empty():
  pool.submit(handle_search,queue_list.get()) # 函数 和参数
.....
```