## .bib文件自动转换脚本

### 功能
将Latex的.bib文件中期刊全称批量转换成缩写

### 依赖
1、bibtexparser

使用bibtexparser可以方便地加载和解析BibTeX文件，安装命令为：
```
# pip
pip install bibtexparser
or
pip3 install bibtexparser

# conda
conda install bibtexparser 
```

2、requests

requests库是一个常用的HTTP库,用于发送HTTP请求和处理响应，安装命令为：
```
# pip
pip install requests
or
pip3 install requests

# conda
conda install requests 
```

3、BeautifulSoup

BeautifulSoup 是一个Python库，主要用于从HTML或XML文件中提取数据。
```
# pip
pip install beautifulsoup4
or
pip3 install beautifulsoup4

# conda
conda install beautifulsoup4 
```

### 运行
1、从Overleaf中下载.bib文件，将bib文件放在与``main.py``相同路径下，并将``BIB_PATH``参数设置为你的bib文件名称；

2、运行``main.py``文件，并手动验证转换失败的条目；

3、替换Overleaf中原有的.bib文件。


### 注意事项
1、如果批量请求失败，请更新网址基准路径

网址为[Science and Engineering Journal Abbreviations](https://woodward.library.ubc.ca/woodward/research-help/journal-abbreviations/)，打开开发者选项（F12），进入Network栏，在页面“Search journal abbreviations:”搜索框中输入任意字符，查看Request URL部分，更新```main.py```中的```BASE_URL```参数即可。如下图所示，将基准网址替换为绿色线段前面的网址就行。

![image text](https://raw.githubusercontent.com/Cool-baby/img-storage/refs/heads/main/for_readme/BibAutoSwitch/bibautoswitch1.png)

2、运行结束之后，会提示运行结果，如果存在错误数据，请手动更正，这可能是因为此网站没有收录。如果失败条数过多，请检查代码中参数设置。