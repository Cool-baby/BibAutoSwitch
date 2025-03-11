# -*- coding: utf-8 -*-

"""
@Author: Zhihao Zhang
@Email: zhang_zhi_hao@foxmail.com
@Date: 2025/3/11 22:23
@Description: bib文件期刊缩写自动化替换
"""
import bibtexparser
import requests
import time
from bs4 import BeautifulSoup
import json
import re
import urllib.parse

# 指定 .bib 文件路径
BIB_PATH = "ref.bib"
# 查询基准地址
BASE_URL = "https://journal-abbreviations.library.ubc.ca/ajaxsearch.php?callback=jQuery112409638803952506474"
# 是否写回原文件（默认True）
WRITE_FLAG = True
# 存储转换成功日志
SUCCESS_LOG = []
# 存储转换失败日志
ERROR_LOG = []


def read_bib_file(file_path):
    """
    读取.bib文件并进行缩写替换
    :param file_path: .bib文件路径
    """
    global TOTAL
    try:
        with open(file_path, 'r', encoding='utf-8') as bib_file:
            bib_database = bibtexparser.load(bib_file)
    except Exception as e:
        print(f"文件读取失败: {e}")
        return

    TOTAL = len(bib_database.entries)  # 计数器

    # 遍历每一条 BibTeX 记录
    for entry in bib_database.entries:
        if entry.get("ENTRYTYPE") == "article":  # 如果当前条目为期刊
            journalName = entry.get("journal", None)  # 获取当前期刊的名称
            if journalName is not None:  # 如果不为空
                # 通过HTTP请求获取缩写
                abbreviation = fetch_journal_abbreviation(journalName)
                if abbreviation is not None:
                    print(f"{journalName} → {abbreviation}")
                    entry["journal"] = abbreviation
                    SUCCESS_LOG.append(entry.get("ID", "Unknown"))
                else:
                    # 记录失败期刊的ID，方便手动修改
                    ERROR_LOG.append(entry.get("ID", "Unknown"))

    # 将修改后的数据写回原文件
    if WRITE_FLAG:
        with open(file_path, 'w', encoding='utf-8') as bib_file:
            bibtexparser.dump(bib_database, bib_file)


def fetch_journal_abbreviation(journalName):
    """
    模拟HTTP请求从缩写查询网站查询最新缩写
    :param journalName: 期刊全称
    :return: 期刊缩写
    """
    timestamp_ms = int(time.time() * 1000)  # 获取当前时间戳
    encoded_text = (urllib.parse.quote(journalName, safe="")
                    .replace("%20", "+")
                    .replace("%5C", "%5C%5C")
                    .replace("%26", "%26"))  # 替换 %20 为 +，并确保 \ 和 & 被正确转换
    url = f"{BASE_URL}_{timestamp_ms}&like={encoded_text}&_={timestamp_ms}"  # 拼接请求URL

    # 发送 GET 请求
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    # 检查 HTTP 响应状态码
    if response.status_code == 200:
        return extract_abbreviation(response.text)
    else:
        print(f"请求失败，状态码：{response.status_code}，请检查基准网址")
        return None


def extract_abbreviation(response_text):
    """
    从HTTP Response中提取出缩写
    :param response_text: Response
    :return: 期刊缩写
    """
    # 提取 JSON 字符串
    json_match = re.search(r"\((\{.*\})\);", response_text)
    if not json_match:
        return None

    json_data = json.loads(json_match.group(1))  # 解析 JSON
    html_content = json_data.get("html", "")

    # 解析 HTML
    soup = BeautifulSoup(html_content, "html.parser")
    abbreviation = soup.find("td")  # 第一个 <td> 是缩写

    return abbreviation.text if abbreviation else None


# 开始转换
read_bib_file(BIB_PATH)

# 打印结果
print("-" * 50)
print(f"运行结束，共有{TOTAL}条数据，成功{len(SUCCESS_LOG)}条，失败{len(ERROR_LOG)}条。")
if len(ERROR_LOG) > 0:
    print("失败期刊ID如下，请手动确认：")
    for entry in ERROR_LOG:
        print(entry)
