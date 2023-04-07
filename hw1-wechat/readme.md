## 安装和使用
后端：
```
cd backend
pip install -r requirements.txt
python main.py
```

前端：
```
cd frontend/wechat
npm install
npm run dev
```

### 测试账号
![[Pasted image 20220513171613.png]]

admin 123

已存在的别的账号：
- u:123, p:123
- u:AXian, p:123
- u:12345, p:12345

确认好友申请：
![[Pasted image 20220513200935.png]]

### 聊天功能

在这次作业中，把私聊抽象成两个人的群聊，
创建聊天群有两个方式：
1. 添加新朋友会自动创建属于两个人的私聊
2. 点击创建群聊 （需要预先添加好友）

![[Pasted image 20220513172002.png]]

![[Pasted image 20220513205909.png]]

发送图片
![[Pasted image 20220513200748.png]]
使用选择文档按钮上传图片并传送给对方

tabbar 查看好友列表

![[Pasted image 20220513210005.png]]
