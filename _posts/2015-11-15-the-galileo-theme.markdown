---
layout: post
title:  "搜狗语音：通讯录优先识别代码说明"
date:   2017-02-20 19:55:14 +0100
categories: Jobs
location: Beijing, China
---


#### 1、文件说明

![图片.png](http://upload-images.jianshu.io/upload_images/1155603-b4878f4cd31cee15.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**SGContact.h** 编译了C++代码，所以引用的地方均需要更名为**.mm**

**SGAddressBook** 用于获取手机通讯录内容

**SGContactData** 包含百家姓本地文件，拼音算法依赖文件

#### 2、使用说明

- 将**SGContact**文件夹添加进工程中 
- 在显示未替换结果的地方导入文件

```
#import "SGContactWrapper.h"
```
- 上屏之前调用替换方法 
```
resultStr = [[SGContactWrapper sharedInstance] convertWithOriginString:resultStr];
```

#### 3、注意事项

- 如果需要(**@optional**)监控是否成功获取通讯录权限以作出响应，实现**SGContactWrapper**的代理方法即可

```
[SGContactWrapper sharedInstance].delegate = self;

- (void)getContactPermissionSuccess:(BOOL)result{
if(result){
// success
}else{
// tell user to get permission
}
}
```

- 目前通迅录的更新条件是联系人姓名信息出现变动，详细实现在**SGContactWrapper.m**中。

- 目前有两种实现方式：

- 获取本地通讯录以.txt文件存到Doument中，对应一种调用方法

```
/**
从本地存的contact.txt文件读取联系人信息

@param originStr 初始字段

@return 跟联系人姓名替换优先级后的结果
*/
- (NSString *)convertWithOriginStr:(NSString *)originStr

```
- 将本地通讯录暂存到**SGContactWrapper**单例的属性(**sgContactArray**)里，对应另一种调用方法，**推荐使用**这一种方法
```
/**
从单例的属性读取联系人信息

@param originString 初始字段

@return 跟联系人姓名替换优先级后的结果
*/
- (NSString *)convertWithOriginString:(NSString *)originString

```
- 涉及要隐私权限，需要在plist文件里添加key值

```
Privacy - Contacts Usage Description
```



