import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const source = fs.readFileSync(new URL('../sources/fusiondemo.js', import.meta.url), 'utf8');
const context = vm.createContext({ Extension: class {} });
vm.runInContext(source.replace('export default class', 'globalThis.Demo = class'), context);
const demo = new context.Demo();
test('three original novels support browsing, search, author and nine chapters', async () => {
  const items = await demo.latest(1);
  assert.equal(items.length, 3);
  assert.equal((await demo.latest(2)).length, 0);
  assert.equal((await demo.search('山间', 1))[0].title, '山间来信');
  assert.equal((await demo.searchAuthor({ name: '聚阅演示' }, 1)).length, 3);
  let chapters = 0;
  for (const item of items) {
    const detail = await demo.detail(item.url);
    assert.equal(detail.episodes[0].urls.length, 3);
    for (const chapter of detail.episodes[0].urls) {
      const result = await demo.watch(chapter.url);
      assert.ok(result.content.join('').length > 200);
      chapters++;
    }
  }
  assert.equal(chapters, 9);
  await assert.rejects(demo.watch('demo:missing/0'));
});
test('no external content request or account API is used', () => {
  assert.equal(/this\.request\(|fetch\(|activation|password/i.test(source), false);
});
