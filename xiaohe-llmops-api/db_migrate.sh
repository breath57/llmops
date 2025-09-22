#!/bin/bash

# ===============================================
# 数据库迁移管理脚本
# 用于管理 xiaohe-llmops-api 项目的数据库迁移
# ===============================================

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 设置环境变量
setup_env() {
    log_info "设置环境变量..."
    
    export FLASK_APP=app.http.app:app
    export FLASK_ENV=development
    
    # Weaviate 配置
    export WEAVIATE_HOST=127.0.0.1
    export WEAVIATE_PORT=8080
    export WEAVIATE_GRPC_PORT=50051
    
    # PostgreSQL 配置
    export SQLALCHEMY_DATABASE_URI="postgresql+psycopg2://llmops:llmops@127.0.0.1:5432/llmops"
    export POSTGRES_HOST=127.0.0.1
    export POSTGRES_PORT=5432
    export POSTGRES_USER=llmops
    export POSTGRES_PASSWORD=llmops
    export POSTGRES_DB=llmops
    
    log_success "环境变量设置完成"
}

# 检查服务状态
check_services() {
    log_info "检查必要服务状态..."
    
    # 检查 PostgreSQL
    if ! docker ps | grep -q postgres-llmops; then
        log_error "PostgreSQL 容器未运行，请先启动："
        echo "docker run --name postgres-llmops -e POSTGRES_DB=llmops -e POSTGRES_USER=llmops -e POSTGRES_PASSWORD=llmops -p 5432:5432 -d postgres:15"
        exit 1
    fi
    log_success "PostgreSQL 服务正常"
    
    # 检查 Weaviate
    if ! docker ps | grep -q weaviate; then
        log_warning "Weaviate 容器未运行，某些功能可能受限"
        echo "启动命令: docker run -d --name weaviate -p 8080:8080 -p 50051:50051 -e WEAVIATE_HOSTNAME=0.0.0.0 semitechnologies/weaviate:latest"
    else
        log_success "Weaviate 服务正常"
    fi
}

# 确保 UUID 扩展已启用
ensure_uuid_extension() {
    log_info "检查并启用 PostgreSQL UUID 扩展..."
    
    if docker exec postgres-llmops psql -U llmops -d llmops -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";" >/dev/null 2>&1; then
        log_success "UUID 扩展已启用"
    else
        log_error "无法启用 UUID 扩展"
        exit 1
    fi
}

# 运行迁移
run_upgrade() {
    log_info "执行数据库迁移..."
    cd "$PROJECT_ROOT"
    
    if uv run flask db upgrade -d internal/migration; then
        log_success "数据库迁移完成"
    else
        log_error "数据库迁移失败"
        exit 1
    fi
}

# 创建新的迁移版本
create_migration() {
    local message="$1"
    if [ -z "$message" ]; then
        log_error "请提供迁移消息"
        echo "使用方法: $0 create '迁移描述'"
        exit 1
    fi
    
    log_info "创建新的迁移版本: $message"
    cd "$PROJECT_ROOT"
    
    if uv run flask db revision --autogenerate -m "$message" -d internal/migration; then
        log_success "迁移版本创建完成"
        log_info "请检查生成的迁移文件并进行必要的调整"
    else
        log_error "创建迁移版本失败"
        exit 1
    fi
}

# 显示当前迁移状态
show_current() {
    log_info "当前数据库迁移状态:"
    cd "$PROJECT_ROOT"
    uv run flask db current -d internal/migration
}

# 显示迁移历史
show_history() {
    log_info "迁移历史:"
    cd "$PROJECT_ROOT"
    uv run flask db history -d internal/migration
}

# 回滚到指定版本
downgrade() {
    local revision="$1"
    if [ -z "$revision" ]; then
        log_error "请提供目标版本"
        echo "使用方法: $0 downgrade [版本号]"
        echo "使用 'base' 回滚到最初状态"
        exit 1
    fi
    
    log_warning "准备回滚到版本: $revision"
    read -p "确认要回滚吗? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cd "$PROJECT_ROOT"
        if uv run flask db downgrade "$revision" -d internal/migration; then
            log_success "回滚完成"
        else
            log_error "回滚失败"
            exit 1
        fi
    else
        log_info "取消回滚操作"
    fi
}

# 初始化数据库
init_db() {
    log_info "初始化数据库..."
    cd "$PROJECT_ROOT"
    
    if uv run flask db init -d internal/migration; then
        log_success "数据库初始化完成"
    else
        log_warning "数据库可能已经初始化过了"
    fi
}

# 重置数据库
reset_db() {
    log_warning "准备重置数据库（删除所有数据）"
    read -p "确认要重置数据库吗? 这将删除所有数据! (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "重置数据库..."
        
        # 删除所有表
        docker exec postgres-llmops psql -U llmops -d llmops -c "
        DROP SCHEMA public CASCADE;
        CREATE SCHEMA public;
        GRANT ALL ON SCHEMA public TO llmops;
        GRANT ALL ON SCHEMA public TO public;
        CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";
        "
        
        log_success "数据库已重置"
        
        # 重新运行迁移
        run_upgrade
    else
        log_info "取消重置操作"
    fi
}

# 显示帮助信息
show_help() {
    echo "数据库迁移管理脚本"
    echo ""
    echo "使用方法:"
    echo "  $0 <命令> [参数]"
    echo ""
    echo "命令:"
    echo "  upgrade              执行数据库迁移（默认操作）"
    echo "  create <message>     创建新的迁移版本"
    echo "  current              显示当前迁移状态"
    echo "  history              显示迁移历史"
    echo "  downgrade <version>  回滚到指定版本"
    echo "  init                 初始化数据库迁移"
    echo "  reset                重置数据库（危险操作）"
    echo "  check                仅检查服务状态"
    echo "  help                 显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0                           # 执行迁移"
    echo "  $0 create 'add user table'   # 创建新迁移"
    echo "  $0 current                   # 查看当前状态"
    echo "  $0 downgrade head-1          # 回滚一个版本"
    echo "  $0 reset                     # 重置数据库"
}

# 主函数
main() {
    case "${1:-upgrade}" in
        "upgrade"|"")
            setup_env
            check_services
            ensure_uuid_extension
            run_upgrade
            ;;
        "create")
            setup_env
            check_services
            create_migration "$2"
            ;;
        "current")
            setup_env
            show_current
            ;;
        "history")
            setup_env
            show_history
            ;;
        "downgrade")
            setup_env
            check_services
            downgrade "$2"
            ;;
        "init")
            setup_env
            check_services
            ensure_uuid_extension
            init_db
            ;;
        "reset")
            setup_env
            check_services
            reset_db
            ;;
        "check")
            check_services
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            log_error "未知命令: $1"
            show_help
            exit 1
            ;;
    esac
}

# 执行主函数
main "$@"
