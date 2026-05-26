---
title: "FGFP"
layout: "projects"
summary: "做过的一些东西"
ShowToc: false
ShowReadingTime: false
ShowWordCount: false
---

## fgvad

智能 VAD 库 —— 在 [ten-vad](https://github.com/TEN-framework/ten-vad) 神经网络 VAD 之上封装状态机和动态尾端点曲线，让"短时命令"和"长时听写"两种场景都有合理的语义切分。

朱志偉一席演讲 25 分钟实测：动态曲线开启 5.9% 强切，关闭 87% 强切——这条曲线是核心竞争力。

Rust 核心 + Swift/Kotlin wrapper。iOS / macOS / Android 三平台。SPM / CocoaPods / JitPack 一行接入。

[GitHub](https://github.com/Fengur/fgvad)

## WindWhisper

macOS 离线语音输入。状态栏 app——点击录音（60s 上限），再点停止，识别结果自动粘贴到光标位置。SenseVoice 离线模型，中英日韩粤五语种自动检测。

[GitHub](https://github.com/Fengur/WindWhisper)

## micvol

macOS 麦克风硬件输入音量控制库 (Rust)。

设备枚举、输入音量控制、VolumeGuard 自动备份/恢复。支持 Cargo、静态库 (.a)、CocoaPods 三种集成方式。

![micvol demo](https://github.com/Fengur/micvol/raw/master/demo.gif)

[GitHub](https://github.com/Fengur/micvol)

## FGDatePicker

iOS UIKit 日期选择弹窗组件。纯 frame 布局，无 Auto Layout。Closure + async/await 双 API。SPM + CocoaPods 接入。

[GitHub](https://github.com/Fengur/FGDatePicker)
