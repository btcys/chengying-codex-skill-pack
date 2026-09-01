import fs from 'node:fs';
import path from 'node:path';

const [url, screenDir, stateDir] = process.argv.slice(2);
if (!url || !screenDir || !stateDir) {
  console.error('用法: node visual-companion-smoke.mjs URL SCREEN_DIR STATE_DIR');
  process.exit(2);
}

async function waitFor(check, label, timeoutMs = 3000) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    const result = await check();
    if (result) return result;
    await new Promise((resolve) => setTimeout(resolve, 50));
  }
  throw new Error(`${label}超时`);
}

const sessionUrl = new URL(url);
const sessionKey = sessionUrl.searchParams.get('key');
if (!sessionKey) throw new Error('启动URL缺少session key');
const cookieName = `brainstorm-key-${sessionUrl.port}`;

const screenPath = path.join(screenDir, 'smoke-layout.html');
fs.writeFileSync(
  screenPath,
  '<h2>可视化冒烟测试</h2><div class="options"><div class="option" data-choice="a" onclick="toggleSelect(this)">方案A</div></div>',
  { encoding: 'utf8', mode: 0o600 },
);

await waitFor(async () => {
  try {
    const response = await fetch(`${sessionUrl.origin}/`, {
      headers: { cookie: `${cookieName}=${sessionKey}` },
    });
    const html = await response.text();
    return response.ok && html.includes('可视化冒烟测试') && html.includes('帧芯可视化设计');
  } catch {
    return false;
  }
}, '服务渲染最新屏幕');

const readyPath = path.join(stateDir, 'screen-ready');
await waitFor(() => {
  if (!fs.existsSync(readyPath)) return false;
  try {
    return JSON.parse(fs.readFileSync(readyPath, 'utf8')).file === 'smoke-layout.html';
  } catch {
    return false;
  }
}, '服务登记新屏幕');

const socketUrl = url.replace(/^http/, 'ws');
const socket = await new Promise((resolve, reject) => {
  const candidate = new WebSocket(socketUrl);
  const timeout = setTimeout(() => reject(new Error('WebSocket连接超时')), 3000);
  candidate.addEventListener('open', () => {
    clearTimeout(timeout);
    resolve(candidate);
  }, { once: true });
  candidate.addEventListener('error', () => {
    clearTimeout(timeout);
    reject(new Error('WebSocket连接失败'));
  }, { once: true });
});
socket.send(JSON.stringify({ type: 'click', choice: 'a', text: '方案A' }));
const eventsPath = path.join(stateDir, 'events');
await waitFor(
  () => fs.existsSync(eventsPath) && fs.readFileSync(eventsPath, 'utf8').includes('"choice":"a"'),
  '浏览器选择事件写入state/events',
);
socket.close();

console.log('Visual Companion冒烟测试通过：启动、鉴权、渲染、交互事件均正常。');
