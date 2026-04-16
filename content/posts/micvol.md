---
title: "micvol：从十年前的一个想法到开源"
date: 2026-04-16
draft: false
tags: ["rust", "macos", "audio", "open-source"]
categories: ["FGZT"]
summary: "把十年前在搜狗做语音识别时的一个工程思路提取出来，做成了开源库。"
---

十年前做语音识别 SDK 的时候，发现一个问题：不同用户的麦克风输入音量设置差异很大，直接影响识别率。

当时的做法是录音前把输入音量拉满，录完恢复。简单粗暴但有效。

最近把这个思路用 Rust 重写了，做成了 [micvol](https://github.com/Fengur/micvol)。核心就一行代码：

```rust
let _guard = micvol::VolumeGuard::maximize(&device.id)?;
// 录音...
// 离开作用域自动恢复
```

支持 Cargo、静态库、CocoaPods 三种集成方式，附带 SwiftUI Demo App。
