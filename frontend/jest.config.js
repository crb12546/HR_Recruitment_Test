/**
 * Jest配置文件
 * 用于配置前端测试环境
 */
module.exports = {
  // 测试环境
  testEnvironment: 'jsdom',
  
  // 转换器配置
  transform: {
    '^.+\\.vue$': '@vue/vue3-jest',
    '^.+\\.js$': 'babel-jest'
  },
  
  // 模块文件扩展名
  moduleFileExtensions: ['vue', 'js', 'json', 'jsx', 'ts', 'tsx', 'node'],
  
  // 测试文件匹配模式
  testMatch: [
    '**/tests/unit/**/*.spec.js',
    '**/tests/components/**/*.spec.js'
  ],
  
  // 模块名称映射
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1'
  },
  
  // 覆盖率收集配置
  collectCoverage: true,
  collectCoverageFrom: [
    'src/**/*.{js,vue}',
    '!src/main.js',
    '!src/router/index.js',
    '!**/node_modules/**'
  ],
  
  // 覆盖率报告目录
  coverageDirectory: '<rootDir>/tests/coverage',
  
  // 测试超时时间
  testTimeout: 10000
};
