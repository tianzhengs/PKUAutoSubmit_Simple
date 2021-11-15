# PKU_AutoSubmit

### 功能 

使用Github Actions, 在每日八点按照上次填报的信息自动填报出入填报

由于填报时使用的是**上次填报的信息**,您应当在您的情况(或填报界面)发生改变时手动重新填报

简化的代码,减少输入参数需要,在填报界面架构不改变情况下应当只需要在界面有修改时手动正确填报(出入校各)一次.如11月中更新后需要选择出校原因类型,需要手动进行出入校各一次正确填报即可,不需要修改仓库和代码

### 使用

填写以下SECRET （名称均为大写）:

​	USERNAME: 门户账号 

​	PASSWORD: 门户密码 

[如何添加SECRET](https://docs.github.com/cn/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository)
