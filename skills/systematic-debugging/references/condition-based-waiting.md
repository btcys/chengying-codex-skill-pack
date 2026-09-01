# 基于条件等待

任意sleep是在猜机器多久能完成工作，容易在CI、并行或高负载下变成竞态。

## 核心原则

等待真正关心的状态、事件、数量或文件出现，并保留明确超时；不要只等待一个估计时长。

```typescript
// 错误：猜50ms足够
await new Promise(resolve => setTimeout(resolve, 50));
expect(getResult()).toBeDefined();

// 正确：等待目标条件
await waitFor(() => getResult() !== undefined, "result is ready");
expect(getResult()).toBeDefined();
```

通用实现：

```typescript
async function waitFor<T>(
  condition: () => T | undefined | null | false,
  description: string,
  timeoutMs = 5000,
): Promise<T> {
  const startedAt = Date.now();
  while (true) {
    const result = condition();
    if (result) return result;
    if (Date.now() - startedAt > timeoutMs) {
      throw new Error(`Timeout waiting for ${description} after ${timeoutMs}ms`);
    }
    await new Promise(resolve => setTimeout(resolve, 10));
  }
}
```

避免1ms高频轮询、无超时循环和在循环外缓存旧状态。

只有测试本身验证debounce、throttle或固定tick等时间语义时，任意等待才合理；先等待触发条件，再按已知时间等待，并用注释说明计算依据。
