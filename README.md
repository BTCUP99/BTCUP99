<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
  <img alt="BTCUP99 · Building handy tools for everyday life" src="assets/banner-light.svg" width="100%">
</picture>

### 🧰 开源项目 · Projects

<a href="https://github.com/BTCUP99/postglow">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/panel-postglow-dark.svg">
    <img alt="Postglow · 账号复盘 — a local Mac app that reviews your X posts" src="assets/panel-postglow-light.svg" width="100%">
  </picture>
</a>

<a href="https://github.com/BTCUP99/jax-stopwatch">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/panel-jax-dark.svg">
    <img alt="jax-stopwatch — push-to-talk AI on your wrist" src="assets/panel-jax-light.svg" width="100%">
  </picture>
</a>

| 项目 | 一句话 | 安装 |
|---|---|---|
| [**Postglow · 账号复盘**](https://github.com/BTCUP99/postglow) | 每小时读一次你的 X 帖子，在本地告诉你哪些帖子被看、什么时候发更好、粉丝从哪来。不用登录、不用 API Key。 | [下载 DMG](https://github.com/BTCUP99/postglow/releases/latest) 或一行命令 |
| [**jax-stopwatch**](https://github.com/BTCUP99/jax-stopwatch) | 把 M5Stack StopWatch 变成 Codex / Webhook Agent 的随身语音入口：按住说话，Mac 帮你办。 | 照着 README 让你的 Agent 帮你装 |

### 💡 做这些小工具时的几点体会 · Notes from building them

- **入口越轻越好。** Jax 是抬手、按住、说一句，比掏手机打字快；Postglow 平时待在菜单栏，每小时读一次，其余时间什么也不做。工具最好的状态是你几乎感觉不到它。<br><sub>The best tool is one you barely notice: a button you press without looking, an app that sits quietly in the menu bar.</sub>
- **本地优先，能不出门的就不出门。** Jax 的语音在 Mac 上用 MLX Whisper 识别，录音不离开电脑；Postglow 的数据只存在你自己的 Mac 上，没有服务器、没有统计上报。<br><sub>Keep audio and data on your own machine; send out only what has to go.</sub>
- **安全要设计进去，而不是事后补。** Jax 的凭据只经 USB 写入，设备只连出不监听；Postglow 的每次更新都用自己的密钥签名，校验通过才会安装。<br><sub>Secrets over the cable only, no listening ports, signed updates.</sub>
- **把不确定的地方说清楚。** 官方不公布粉丝来源，Postglow 的「涨粉从哪来」就明确标成估算、仅供参考；没有付费做 Apple 公证，就如实写清 macOS 为什么会提示「已损坏」以及怎么打开。<br><sub>Say plainly what's an estimate and what the trade-offs are.</sub>
- **文档也是产品。** Jax 的安装步骤写到 Agent 能照做的程度，用户只需要一句话；Postglow 的每个板块旁边都有一个 **?**，鼠标停上去就知道它在算什么。<br><sub>Write docs an agent can follow, and put the explanation right where the number is.</sub>

<sub>更多实用工具在路上 · More tools on the way. 欢迎 Star、Issue 和 PR。</sub>
