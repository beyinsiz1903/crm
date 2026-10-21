import {describe, it, expect, vi} from 'vitest';
import {createSaveQueue, operationError} from './saveQueue';

describe('reliable saves', () => {
  it('serializes slow older saves before the newest edit', async () => {
    let unblock;
    const calls = [];
    const write = vi.fn(async data => {calls.push(data); if (data.v === 1) await new Promise(resolve => {unblock = resolve;});});
    const save = createSaveQueue(write);
    const first = save({v: 1});
    const newest = {v: 2};
    const second = save(newest);
    newest.v = 3;
    await new Promise(resolve => setTimeout(resolve, 0));
    expect(calls).toEqual([{v: 1}]);
    unblock(); await first; await second;
    expect(calls).toEqual([{v: 1}, {v: 2}]);
  });
  it('reports failure but allows a later retry', async () => {
    const save = createSaveQueue(vi.fn().mockRejectedValueOnce(new Error('offline')).mockResolvedValueOnce('ok'));
    await expect(save({v: 1})).rejects.toThrow('offline');
    await expect(save({v: 2})).resolves.toBe('ok');
  });
  it('shows actionable publication errors', () => {
    expect(operationError({response: {data: {detail: {issues: ['Configure booking', 'Configure hosting']}}}})).toContain('Configure hosting');
  });
});
