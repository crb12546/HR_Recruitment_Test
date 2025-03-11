/**
 * 示例单元测试文件
 * 用于演示如何编写基础测试
 */

describe('基础测试示例', () => {
  test('基本断言示例', () => {
    // 基本断言
    expect(1 + 1).toBe(2);
    expect('Hello').toContain('ello');
    expect([1, 2, 3]).toHaveLength(3);
    expect({ name: '张三', age: 30 }).toHaveProperty('name', '张三');
  });
});
