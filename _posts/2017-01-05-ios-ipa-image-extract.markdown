---
layout: posts
title:  "the-galileo-theme"
date:   2017-01-05 00:00:00 +0100
categories: Jobs
author_profile: true
---

作为一个移动端开发人员，经常要扒一扒其他项目的图片资源，可以用来直接使用或者做预开发时的占位图，也可以通过分析一个 ipa 中的图片资源来推导某一个功能的实现原理，简而言之，扒图也是开发人员应该具有的一个技能。考虑到年纪到了，忘东西越来越快，明年后年可能忘得更快，记一帖当做笔记。

###### 1. 获取目标 ipa

比如你要看一下 QQ 里都用到了哪些图片，首先要做得就是弄一个 QQ 的 ipa，获取 ipa 方式多种多样，如 iTunes 获取、iTools 获取等等，这里选用 iTunes 来获取 **QQ6.6.2.ipa**。

![0F49305C-B184-4C81-906A-0353475B8D50.png](http://upload-images.jianshu.io/upload_images/1155603-4c52416a1888486e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

搜索你想要查找的项目名称，然后点击 **获取**，下载完成就能在 **资料库** 里看到了。

![FDDDCDF3-C6CC-4484-8ED4-69FF84A12C7F.png](http://upload-images.jianshu.io/upload_images/1155603-9428a8fd07f52b41.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###### 2. 拆解目标 ipa

将 **QQ6.6.2.ipa** 拓展名改为 **.zip** 后解压。

![DD30A4FC-A9F2-420A-97AD-AC13EDBD5A65.png](http://upload-images.jianshu.io/upload_images/1155603-3e974c62f4e34b89.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

此处插播一条题外消息，在包内容中也可以看到该工程的 **plist** 文件，感兴趣的同学也可以在这用拿到配置文件原型来啃一啃。

![图片.png](http://upload-images.jianshu.io/upload_images/1155603-2713b7a5d6ada0a9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

接下来将刚才 **查看包内容** 后的文件夹单独拷贝出来，用一个单独文件夹接收，这是为了避免每次查看都要经过 **显示包内容** 操作。

![图片.png](http://upload-images.jianshu.io/upload_images/1155603-53eefebe28727407.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**ipa** 的资源已经拆解完毕，可以简单预览一下。

![图片.png](http://upload-images.jianshu.io/upload_images/1155603-90eb7ac2acbb8056.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![图片.png](http://upload-images.jianshu.io/upload_images/1155603-6550fdbf632c20e9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![图片.png](http://upload-images.jianshu.io/upload_images/1155603-56505ed9774cc335.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![图片.png](http://upload-images.jianshu.io/upload_images/1155603-ab3e820d0330dd61.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![图片.png](http://upload-images.jianshu.io/upload_images/1155603-5b5bd53772c13e57.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![图片.png](http://upload-images.jianshu.io/upload_images/1155603-7e409d61979170ea.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![图片.png](http://upload-images.jianshu.io/upload_images/1155603-eee6bd2fcf2ac182.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

还有其他如 nib 文件、使用 SDK 相关信息、工程热更新代码配置等等都可以从这个包的内容里看到蛛丝马迹甚至部分源码。

###### 3. 获得 Images.xcassets 中的图片

因为 QQ 的主题和自定义装扮配置较多，本地资源图片几乎全部暴露在 bundle 路径，所以经过上面几步的拆解，大部分图片资源都已经可以获得，但是现在很多本地资源的图片我们都放在了 **Image.xcassets** 中。

![图片.png](http://upload-images.jianshu.io/upload_images/1155603-f0b803d6e541d0b5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这个文件夹里的图片，在打包成 **ipa** 的时候 Xcode 会单独给它设置路径，形成一个新的文件显示在包内容中，这里以斗鱼的 **ipa** 来做示例。

![图片.png](http://upload-images.jianshu.io/upload_images/1155603-ebe2ae8e593108e2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![图片.png](http://upload-images.jianshu.io/upload_images/1155603-44e908ffe5b2c787.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

到了这一步，最关键的 **Assets.car** 文件已经浮出水面了。

###### 4. 利用 cartool 来解析 Assets.car

1. clone 或者 download [cartool](https://github.com/steventroughtonsmith/cartool)
2. 按照自己对于 source 资源的需求修改 cartool 内代码

此处仅演示获取资源，所以将这部分代码修改如下：

```objc
NSString *idiomSuffixForCoreThemeIdiom(kCoreThemeIdiom idiom)
{
    return @"";
}
```

3. 将上一步获得的 **Assets.car** 拷贝到一个方便找到的位置，并新建一个文件夹来接收 **Assets.car** 中的图片。

![图片.png](http://upload-images.jianshu.io/upload_images/1155603-28277344a5491bf9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

4. 给 cartool 修改 **Scheme**

![图片.png](http://upload-images.jianshu.io/upload_images/1155603-d3f75a3522cb2225.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

将上一部准备好的 **Assets.car** 和接收文件拖入到如下位置：

![图片.png](http://upload-images.jianshu.io/upload_images/1155603-3f26b81de8faf546.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**MARK：** 此处的顺序是固定的，不要弄反。

5. Run **cartool**

此时 log 中有一大堆资源的名字陆续出来，这就代表本次解析图片已经成功。

![图片.png](http://upload-images.jianshu.io/upload_images/1155603-6f286788b9b702d2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

此时去查看接收文件的文件夹。

![图片.png](http://upload-images.jianshu.io/upload_images/1155603-2bae101b58199e95.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

所有 **Accests.car** 中的图片已经拿到。

![图片.png](http://upload-images.jianshu.io/upload_images/1155603-c0a41c08a2187ec6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这波 **ipa** 图片资源文件获取步骤已经差不多讲完，看起来很繁琐，其实很简单，就是一个熟练度的事情，忘记了的时候随时来瞅一眼就好，这也是笔记最合理的存在原因了，谢谢观众老爷的赏光。