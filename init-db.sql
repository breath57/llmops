-- PostgreSQL 数据库初始化脚本
-- 用于Docker Compose自动初始化

-- 启用UUID扩展（LLMOps项目需要）
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 创建必要的索引和约束（如果需要）
-- 这些可以根据项目的具体需求进行调整

-- 输出初始化完成信息
DO $$
BEGIN
    RAISE NOTICE '数据库初始化完成！UUID扩展已启用。';
END $$;
