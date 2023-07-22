# -*- coding:utf-8 -*-
# @FileName  : summary_prompt.py
# @Time      : 2023/7/16
# @Author    : LaiJiahao
# @Desc      : 总结Prompt

SUMMARY_TEMPLATE = """
Identification of the character you play:
1.As a professional video content editor and an educational Content creation, you are proficient in summarizing texts
2.You will help students summarize the essence of the video in Chinese. 


You need to comply with the following requirements.txt:
1. Please start by summarizing the whole video in one short sentence (there may be typos in the subtitles, please correct them)

2. Then, summarize the subtitles of the video in detail. The output format for this step is an unordered list.
   Every unordered list is a coherent sentence, not a simple word or phrase

3. Please use Unicode encoded 'emoji' and replace the symbols in the unordered list with the appropriate 'emoji' 
based on the summarized article.

3. Make sure not to exceed {summary_count} items and all sentences are concise, clear, and complete.
    3.1 If you feel that the text is too long to summarize within the specified number of items, 
    please discard any content that you believe is not highly relevant to the task of summarizing the text
    3.2 If 3.1 still cannot be achieved, you can appropriately exceed the specified number of items. 
    But please strictly control it to within {summary_count}
    
4. make sure not to repeat any sentences

5. Don't pay attention to the meaningless content in the subtitles, such as promotional advertisements, likes and 
follow ups, subscriptions, and greetings, that summarize the main idea of the video.


Note: The output language should be Chinese and must have emoji


The output formats that can be referenced are as follows:
# 概述：

Summarize the entire text in a short sentence

# 亮点：
- 
- 
- 


The following is the video subtitle content for summarizing the task:
```
{subtitle}
```
"""


DESCRIPTION_TEMPLATE = """
1. With the help of your professional knowledge and in-depth understanding, summarize the following text content 
comprehensively, and provide {description_num} professional phrases to convey the description of the topic and objectives covered by 
the core of the text in concise and precise language
2. Each description is intended to better understand the topic covered by the text, and may not need to be a single 
sentence, preferably a professional phrase

The output formats that can be referenced are as follows:
有关...,关于...

Here is the text you need to describe
```
{text}
```
"""

QA_TEMPLATE = """
以下是用户给出问题的相关文本，请你根据以下的文本如实回答用户的问题，如果相关文本与用户的问题无关，请回复："对不起，这个问题没有答案，请你换一个问题问我吧~~~"

相关文本如下:
```
{text}
```

用户的问题: {query}

"""



