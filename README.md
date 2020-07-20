# DOTA2监视下分小助手

一个用来监视队友下分的小工具, 当打完一场对局后会自动将对局详情发送到聊天工具, 目前仅支持Discord.

在使用之前, 请编辑*contents.py*的*WEBHOOKS*变量以添加频道Webhook url以及*PERSON*添加player id以及昵称.

需要安装requests, 使用以下命令来安装

```
python -m pip install -r requirements.txt
```

初次使用推荐 `python task.py -f` 来避免发送过多比赛详情.

之后使用 `python task.py` 来运行就好.

如果不喜欢初始语句的话可以编辑**WIN_NEGATIVE, WIN_POSTIVE, LOSE_NEGATIVE, LOSE_POSTIVE**四个变量来修改.