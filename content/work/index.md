---
title: "Work"
layout: "projects"
summary: "Open-source libraries"
ShowToc: false
ShowReadingTime: false
ShowWordCount: false
---

Small, focused libraries for voice activity detection, audio I/O, and macOS tooling. Most are extracted from past speech SDK work experience, refined into reusable open-source components.

## fgvad

Smart VAD with dynamic endpointing, on top of [ten-vad](https://github.com/TEN-framework/ten-vad). Knows when speakers actually stop talking, not just when sound stops. **5.9% force-cut rate vs 87%** on a real 25-minute lecture when the dynamic tail curve is disabled.

Rust core + Swift / Kotlin wrappers. iOS 16+ / macOS 13+ / Android API 26+. SPM + CocoaPods + JitPack — one-line integration on each platform.

[GitHub](https://github.com/Fengur/fgvad)

## WindWhisper

Offline voice input for macOS. Status bar app — click to record (up to 60s), click again to stop, transcript pasted to cursor. SenseVoice int8 model, Chinese / English / Japanese / Korean / Cantonese auto-detect, all offline.

[GitHub](https://github.com/Fengur/WindWhisper)

## micvol

macOS hardware-level microphone input volume control via CoreAudio HAL. Maximize input gain at the A/D conversion stage instead of digital AGC. Cargo crate + static library + CocoaPods.

![micvol demo](https://github.com/Fengur/micvol/raw/master/demo.gif)

[GitHub](https://github.com/Fengur/micvol)

## FGDatePicker

Lightweight UIKit date picker modal. Pure frame-based layout, no Auto Layout. Closure + async/await dual API. SPM + CocoaPods.

[GitHub](https://github.com/Fengur/FGDatePicker)

---

Previously: 5+ years on a wearable voice SDK. Earlier: speech recognition SDK work. The boundary between VAD and ASR — endpoint detection strategy, dynamic thresholds, audio gain at the analog / digital interface — is where these libraries come from.
