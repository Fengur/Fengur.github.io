var store = [{
        "title": "the-galileo-theme",
        "excerpt":"作为一个移动端开发人员，经常要扒一扒其他项目的图片资源，可以用来直接使用或者做预开发时的占位图，也可以通过分析一个 ipa 中的图片资源来推导某一个功能的实现原理，简而言之，扒图也是开发人员应该具有的一个技能。考虑到年纪到了，忘东西越来越快，明年后年可能忘得更快，记一帖当做笔记。 1. 获取目标 ipa 比如你要看一下 QQ 里都用到了哪些图片，首先要做得就是弄一个 QQ 的 ipa，获取 ipa 方式多种多样，如 iTunes 获取、iTools 获取等等，这里选用 iTunes 来获取 QQ6.6.2.ipa。 搜索你想要查找的项目名称，然后点击 获取，下载完成就能在 资料库 里看到了。 2. 拆解目标 ipa 将 QQ6.6.2.ipa 拓展名改为 .zip 后解压。 此处插播一条题外消息，在包内容中也可以看到该工程的 plist 文件，感兴趣的同学也可以在这用拿到配置文件原型来啃一啃。 接下来将刚才 查看包内容 后的文件夹单独拷贝出来，用一个单独文件夹接收，这是为了避免每次查看都要经过 显示包内容 操作。 ipa 的资源已经拆解完毕，可以简单预览一下。 还有其他如 nib 文件、使用 SDK 相关信息、工程热更新代码配置等等都可以从这个包的内容里看到蛛丝马迹甚至部分源码。 3. 获得 Images.xcassets...","categories": ["Jobs"],
        "tags": [],
        "url": "/jobs/2017/01/04/ios-ipa-image-extract/",
        "teaser": null
      },{
        "title": "搜狗语音：通讯录优先识别代码说明",
        "excerpt":"1. 文件说明 SGContact.h 编译了 C++ 代码，所以引用的地方均需要更名为 .mm SGAddressBook 用于获取手机通讯录内容 SGContactData 包含百家姓本地文件，拼音算法依赖文件 2. 使用说明 将 SGContact 文件夹添加进工程中 在显示未替换结果的地方导入文件 #import \"SGContactWrapper.h\" 上屏之前调用替换方法 resultStr = [[SGContactWrapper sharedInstance] convertWithOriginString:resultStr]; 3. 注意事项 如果需要（@optional）监控是否成功获取通讯录权限以作出响应，实现 SGContactWrapper 的代理方法即可 [SGContactWrapper sharedInstance].delegate = self; - (void)getContactPermissionSuccess:(BOOL)result{ if(result){ // success }else{ // tell user to get permission } } 目前通讯录的更新条件是联系人姓名信息出现变动，详细实现在 SGContactWrapper.m...","categories": ["Jobs"],
        "tags": [],
        "url": "/jobs/2017/02/20/sougou-contact-code-explain/",
        "teaser": null
      }]
