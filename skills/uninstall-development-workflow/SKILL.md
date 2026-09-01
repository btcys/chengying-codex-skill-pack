---
name: uninstall-development-workflow
description: 仅当用户明确要求卸载、移除或停用帧芯开发工作流插件时使用；通过Codex官方插件卸载能力移除安装和缓存，并默认保留插件源文件与所有项目资料。
---

# 一键卸载帧芯开发工作流

本Skill只能显式调用，不因清理、归档、分支收尾或项目完成自动触发。用户明确要求卸载即构成卸载授权，不再追加确认。

## 卸载范围

默认只移除Codex中的插件安装记录和缓存：

```text
zhenxin-development-workflow@<marketplace>
```

默认保留：

- 插件源码和压缩包；
- marketplace定义；
- 项目中的PRD、ROADMAP、Spec、Plan、截图和发布记录；
- 项目中的 `.codex/execution/`；
- Git分支、worktree、commit和用户代码。

只有用户明确要求删除上述特定资料时，才把它作为独立清理任务处理；插件卸载本身不得删除。

## 一键流程

1. 检查 `codex plugin` 命令存在；不存在时报告当前环境无法自动卸载，不使用文件删除模拟。
2. 运行只读命令：

   ```bash
   codex plugin list --available --json
   ```

3. 在 `installed` 中精确匹配 `name == "zhenxin-development-workflow"`；不要猜marketplace。
4. 未安装时报告“当前未安装”，成功结束，不改任何文件。
5. 只匹配一个时执行：

   ```bash
   codex plugin remove zhenxin-development-workflow@<marketplace> --json
   ```

6. 匹配多个marketplace时，列出准确选择并让用户指定；不得批量卸载。
7. 再运行一次list，确认目标不再出现在 `installed`；失败时报告原始错误和当前状态，不手动清缓存。
8. 提醒用户新开Codex任务，使当前会话不再继续使用已经加载的Skill。

如果运行环境提供专门的插件卸载工具，优先使用该工具完成第5～7步；其目标仍必须是准确的插件ID。

没有专用工具时，先把 `SKILL_DIR` 解析为当前这份 `SKILL.md` 所在目录，再运行确定性脚本；不得以用户项目当前目录解析相对路径：

```bash
python3 "$SKILL_DIR/scripts/uninstall.py"
```

仅在检测到多个同名安装且用户已指定marketplace时传入；指定值必须精确匹配当前安装，否则脚本拒绝卸载：

```bash
python3 "$SKILL_DIR/scripts/uninstall.py" --marketplace <exact-name>
```

## 禁止

- 不直接删除 `~/.codex`、`~/.agents` 或缓存目录；
- 不手工编辑Codex配置或marketplace文件；
- 不卸载Visualize、Browser或其他依赖插件；
- 不删除项目中的 `.codex/`；
- 不用模糊名称匹配或通配符；
- 不宣称当前已加载的Skill会在同一会话即时消失。
