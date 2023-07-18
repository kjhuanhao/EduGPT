# EduGPT




# 开发规范

切换分支
```shell
git chekout 分支名
```

```shell
git add -A
git commit -m "描述本次修改的内容"
git push 
```

拉代码
```shell
git pull origin main 
```

# Gradio设计思路
## 成绩分析模块
核心思路：将大模型生成的代码进行抽离，注入python中，作为本地函数，将plot的对象进行返回给组件

## 刷题模块
核心思路：放入了一个local_state，用于动态更新题型，解决了题目切换，遇到不同题型的问题