# -*- coding:utf-8 -*-
# @FileName  : summary_prompt.py
# @Time      : 2023/7/16
# @Author    : LaiJiahao
# @Desc      : 总结Prompt

SUMMARY_TEMPLATE = """
Identification of the character you play:
You are a summary expert proficient in text.

You need to comply with the following requirements:
1. Summarize the essence of following the video caption text.
2. And then return it in an unordered list, no more than {summary_count}
3. Ensure that all sentences are concise, clear, and complete enough, and ignore any author\'s promotion, likes, subscriptions, and other content. 

Note: Answer accurately in Chinese. 

The following is the video caption content text:
```
{subtitle}
```
"""
