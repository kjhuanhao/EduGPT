# EduGPT
该项目从教师和学生的角色出发，结合大语言模型开发的AI应用，为教育降本增效的AI应用，让教育更加智能化，让学习更加高效化

## 项目介绍

### 项目特色
- 教师智能成绩分析，可上传成绩单，生成各类图表以及与数据的智能分析
- 学生在线刷题工具，根据大模型生成的题库，可在线刷题，拥有获取提示、获取题目答案、学生答案分析等功能
- 智能题目生成，可以根据简单的描述，智能生成题目
- 智能网课总结，上传音频或者视频，或者在线网课的链接，智能生成文字总结，还可以根据网课内容生成题目
- 学习计划制定
- 语文作文评分
- 学习视频推荐(调用B站API)
- 启发式学习，提高学生的思辨能力

### 我们为什么要做这样一个项目
起因是报名参加了[百度飞桨的2023大模型应用创新挑战赛](https://aistudio.baidu.com/aistudio/competition/detail/998/0/introduction)
同时我们也是两名学生，于是敲定主题，做教育相关的AI应用


## 项目展示



## 项目结构
- common: 通用的工具类
- entity: 实体类
- exception: 异常类
- prompt: 封装prompt信息
- resources: 资源文件
- service: 业务层，负责app与其他方法的交互
- util: 工具类

## 项目运行环境
- python 3.11

## 项目启动
首先请确保你安装了本项目的运行环境
```shell
pip install -r requirements.txt.txt
```

然后执行以下命令启动
```shell
python3 app.py
```

## 参考资料&项目
- https://github.com/Aomferni/chatTests
- https://github.com/JimmyLv/BibiGPT


## 关于项目成员
- [赖佳豪](https://laijiahao.cn/) 专业：会计学
- [林子豪]() 专业：英语
