// A hard timeout that does NOT rely on fetch/AbortController actually
// honoring cancellation (some RN/device combos don't). It races the given
// promise against a plain JS timer, so the caller always gets a
// resolve/reject within timeoutMs, even if the underlying request is still
// hanging in the background.
function withHardTimeout<T>(promise: Promise<T>, timeoutMs: number): Promise<T> {
  return new Promise<T>((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error('timeout')), timeoutMs);
    promise.then(
      (value) => {
        clearTimeout(timer);
        resolve(value);
      },
      (err) => {
        clearTimeout(timer);
        reject(err);
      }
    );
  });
}

export async function fetchWithTimeout(url: string, timeoutMs = 12000, init?: RequestInit): Promise<Response> {
  const controller = new AbortController();
  const abortTimer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    return await withHardTimeout(fetch(url, { ...init, signal: controller.signal }), timeoutMs + 1000);
  } finally {
    clearTimeout(abortTimer);
  }
}

// Runs `task` over `items` with at most `limit` running at once, instead of
// firing everything in parallel — friendlier to weak/mobile connections and
// avoids piling up dozens of simultaneous requests on one screen.
export async function runWithConcurrency<T>(
  items: T[],
  limit: number,
  task: (item: T) => Promise<void>
): Promise<void> {
  let index = 0;
  async function worker() {
    while (index < items.length) {
      const current = items[index++];
      await task(current);
    }
  }
  const workerCount = Math.min(limit, items.length);
  await Promise.all(Array.from({ length: workerCount }, worker));
}
