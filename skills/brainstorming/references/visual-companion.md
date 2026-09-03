# Visual Companion

只在“看见比文字更容易判断”时使用。它是需求讨论中的可视化工具，不是独立开发阶段或第二套产品工程。

## 必须使用

- 新页面或新入口；
- 页面结构和布局大改；
- 复杂交互或跨页面设计规则；
- 必须比较两个以上视觉方案；
- 需要在开发前确认关键状态。

文字范围、接口、数据模型和普通技术取舍不使用可视化。

外部设计参考只在新项目没有Design-Brief、新页面没有现成模式、现有规范无法判断，或用户连续两轮明确不满意时查；普通小改不查。

## 可展示内容

- 浏览器mockup和线框；
- 两到四个布局或视觉方案；
- 默认、加载、空、错误、禁用、成功等相关状态；
- 页面流、组件关系和架构图；
- 可点击的单选或多选项。

优先使用当前Codex环境提供的会话内可视化或浏览器能力。宿主没有可交互可视化能力时，使用本Skill自带的本地Companion；它只是设计会话，不是产品Preview工程，不创建产品路由或引入项目依赖。

## 展示方式

### A. 宿主原生可视化（优先）

若Codex当前环境可直接展示可交互HTML、浏览器页面或图表，直接复用该会话能力。每轮只保留本轮问题和选项，选择结果仍按下方“确认输出”写回Spec。

### B. 本地Companion（回退）

宿主能力不足时，先把当前 `brainstorming` Skill目录解析为 `SKILL_DIR`，再启动。脚本默认以前台模式运行；在Codex中让命令保持为持久终端会话，不要自行追加 `&`：

```bash
"$SKILL_DIR/scripts/start-server.sh" --project-dir <project-root> --open
```

启动结果是JSON，至少包含：

```json
{"type":"server-started","url":"http://localhost:<port>/?key=<session-key>","screen_dir":"<session>/content","state_dir":"<session>/state"}
```

- 保存完整 `url`、`screen_dir`、`state_dir` 和session目录；URL中的 `key` 不得删掉或公开转发；
- 持久文件位于 `<project-root>/.codex/visual-companion/`，不得写入旧工作流目录；
- 只有宿主明确拥有可靠的后台任务生命周期时才传 `--background`；Codex默认保持前台持久会话；
- `--open` 只在用户已经同意进入可视化选择时使用；无法自动打开时提供完整URL作为回退；
- 不把session key、PID、日志或事件文件提交到Git。

服务脚本：[start-server.sh](../scripts/start-server.sh)、[stop-server.sh](../scripts/stop-server.sh)。脚本使用Node.js标准库，不给产品安装依赖。

## 本地Companion循环

1. 写屏幕前重新运行同一启动命令：已有进程仍存活时脚本直接返回原 `server-info`；进程已失效时标记旧session并新建会话。首选端口空闲时复用端口和key；端口仍被占用时返回新的完整URL，不继续使用旧URL。
2. 向 `screen_dir` 写一个新的语义化HTML文件，例如 `dashboard-layout.html`、`dashboard-layout-v2.html`；不得复用旧文件名。
3. 默认只写HTML片段。服务会补齐主题、连接状态和交互脚本；确需完整控制时才写完整HTML文档。
4. 告诉用户当前展示的问题和方案，让用户在页面点击并在对话中确认。对话文字是主反馈，浏览器事件是补充证据。
5. 下一轮读取 `state_dir/events`。每行是一个JSON事件，例如：

   ```json
   {"type":"click","choice":"b","text":"Option B","timestamp":1706000115}
   ```

6. 反馈改变当前方案时生成新版本屏幕；当前问题确认后才进入下一个视觉问题。
7. 返回纯文字讨论时推送简单等待页，避免浏览器继续显示已失效方案。
8. 结束后执行：

   ```bash
   "$SKILL_DIR/scripts/stop-server.sh" <exact-session-dir>
   ```

停止脚本只终止能用session instance ID证明归属的进程；PID含糊时拒绝误杀。项目内会话证据默认保留，`/tmp`临时session才自动清理。

### 最小可交互片段

```html
<h2>选择工作台布局</h2>
<p class="subtitle">比较信息层级、常用入口和画布空间</p>
<div class="options">
  <div class="option" data-choice="a" onclick="toggleSelect(this)">
    <div class="letter">A</div><div class="content"><h3>左侧工具栏</h3><p>画布空间更完整</p></div>
  </div>
  <div class="option" data-choice="b" onclick="toggleSelect(this)">
    <div class="letter">B</div><div class="content"><h3>双侧面板</h3><p>属性编辑更直接</p></div>
  </div>
</div>
```

多选时给 `.options` 增加 `data-multiselect`。布局比较可使用内置 `.cards`、`.mockup`、`.split`、`.pros-cons`、`.mock-nav`、`.mock-sidebar` 和 `.mock-content`。

## 每轮规则

1. 一次只解决一个视觉问题，例如布局或错误态；
2. 每屏最多四个方案；
3. 使用接近真实的内容和信息密度；
4. 线框解决结构，精细稿解决视觉，不提前追求像素级完成；
5. 用户选择后记录最终决定和必要取舍；
6. 反馈改变当前方案时先迭代当前屏，不急着进入下一个问题。

## UI确认前检查

请求用户确认新页面或重大UI前，必须完成三项检查；任一项未完成时只能称为内部草稿：

1. **组件复用**：先检查项目已有组件、设计系统和交互模式。能复用就不另造；必须新增时说明缺口、复用边界和新增组件职责。
2. **设计规范**：先读取 `Design-Brief.md` 和相关设计域，明确使用的Token、字体、颜色、间距、图标、响应式、主题和无障碍约束；没有 Design-Brief 时先建立并确认最小规范，不得只凭当前mockup临时写一套样式。
3. **状态与动效**：覆盖与本次范围有关的默认、hover/focus/press、加载、空、错误、禁用、成功和切换状态；重要动效写清用途、触发、起止状态、时长、缓动、能否中断和减弱动效路径。

动效用于反馈、连续性和状态理解，不为普通工具页面堆装饰。一个页面最多保留一到两个品牌性动效，其余保持短而功能化。简单状态优先CSS和项目已有能力；不为普通淡入、hover或弹窗单独增加动效依赖。优先动画 `transform` 和 `opacity`，避免布局跳动，并支持 `prefers-reduced-motion` 或目标平台的等价能力。

已有Design-Brief但缺少本次局部规则时，在当前Spec定义最小Token和动效合同；项目完全没有Design-Brief时先建立并确认它。

如果项目完全没有 `Design-Brief.md`，且本次范围包含新页面、跨页面规则或重大改版，应先补一份最小 Design-Brief 并取得确认；页面级细节仍写入当前 Spec。

## 确认输出

将确认结果写入Spec：

- 页面或入口；
- 选定布局和拒绝方案；
- 关键交互；
- 状态矩阵；
- 响应式边界；
- 组件和Token约束；
- 状态与动效合同；
- `UI Compliance`：组件复用、设计规范、状态与动效分别标记 `PASS` 或写明已批准例外；
- `Design-Brief`：记录使用的版本；只有跨页面或全局规则变化才回写该文档；
- 相关Golden或证据ID。

确认结果进入Plan的 `Global Constraints`，开发直接实现真实UI与功能。产品验收负责比较实际页面和确认稿。

用户确认的是设计决定，不是浏览器中的最后一次点击。最终选择必须在对话中明确，并写入Spec；需要作为Golden的页面或截图按产品治理规则取得Evidence ID，普通探索稿不长期归档。

## 安全与记录

- 不在可视化内容中放Secret、生产数据或个人信息；
- 会话选择只作为设计证据，不替代用户在对话中的明确确认；
- 若宿主管理session、进程和连接，复用宿主能力，不自行复制PID或后台服务系统；
- 临时文件放在任务授权目录，项目内证据按产品治理规则归档。
- 可视化服务默认只绑定loopback；只有远程环境确实需要时才改变host，并继续使用完整session key；
- 不加载远程品牌图片、不发送遥测，不把项目数据交给第三方页面。
