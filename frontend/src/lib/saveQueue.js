// Serialize saves so a slow autosave cannot overwrite a newer manual save.
export function createSaveQueue(write) {
  let queue = Promise.resolve();
  return value => {
    const snapshot = JSON.parse(JSON.stringify(value));
    queue = queue.catch(() => {}).then(() => write(snapshot));
    return queue;
  };
}

export function operationError(error) {
  const detail = error?.response?.data?.detail;
  if (typeof detail === 'string') return detail;
  if (detail?.issues) return detail.issues.join('\n');
  return 'İşlem tamamlanamadı. Değişiklikleri koruyup yeniden deneyin.';
}
