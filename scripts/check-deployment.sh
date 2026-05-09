#!/bin/bash

# FDE Workbench 部署前检查脚本
# 用途：在部署前自动检查所有配置，避免运行时错误

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0
WARNINGS=0

echo "======================================"
echo "  FDE Workbench 部署前检查"
echo "======================================"
echo ""

# 1. 检查 Docker 服务状态
echo "📦 1. 检查 Docker 容器状态..."
REQUIRED_CONTAINERS=("mysql-8.0" "redis" "fde-mate-ai")
for container in "${REQUIRED_CONTAINERS[@]}"; do
    if docker ps --format '{{.Names}}' | grep -q "^${container}$"; then
        echo -e "  ${GREEN}✓${NC} $container 运行中"
    else
        echo -e "  ${RED}✗${NC} $container 未运行"
        ERRORS=$((ERRORS + 1))
    fi
done
echo ""

# 2. 检查端口占用
echo "🔌 2. 检查端口占用..."
PORTS=(5173 8080 8090 3306 6379)
for port in "${PORTS[@]}"; do
    if lsof -i :$port > /dev/null 2>&1; then
        echo -e "  ${GREEN}✓${NC} 端口 $port 已被占用"
    else
        echo -e "  ${YELLOW}⚠${NC} 端口 $port 空闲"
        WARNINGS=$((WARNINGS + 1))
    fi
done
echo ""

# 3. 检查数据库连接
echo "🗄️  3. 检查数据库连接..."
if docker exec mysql-8.0 mysql -uroot -p20260227 -e "SELECT 1" > /dev/null 2>&1; then
    echo -e "  ${GREEN}✓${NC} MySQL 连接正常"
else
    echo -e "  ${RED}✗${NC} MySQL 连接失败"
    ERRORS=$((ERRORS + 1))
fi

if docker exec redis redis-cli ping > /dev/null 2>&1; then
    echo -e "  ${GREEN}✓${NC} Redis 连接正常"
else
    echo -e "  ${RED}✗${NC} Redis 连接失败"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# 4. 检查 API 配置
echo "⚙️  4. 检查 API 配置..."
API_URL=$(docker exec fde-mate-api env 2>/dev/null | grep DATABASE_URL || echo "")
if echo "$API_URL" | grep -q "mysql-8.0"; then
    echo -e "  ${GREEN}✓${NC} DATABASE_URL 主机名正确 (mysql-8.0)"
elif echo "$API_URL" | grep -q "shared-mysql"; then
    echo -e "  ${RED}✗${NC} DATABASE_URL 使用了错误的主机名 (shared-mysql)"
    ERRORS=$((ERRORS + 1))
else
    echo -e "  ${YELLOW}⚠${NC} DATABASE_URL 未找到或格式异常"
    WARNINGS=$((WARNINGS + 1))
fi

if echo "$API_URL" | grep -q "root:20260227"; then
    echo -e "  ${GREEN}✓${NC} DATABASE_URL 凭证正确"
elif echo "$API_URL" | grep -q "fde_user"; then
    echo -e "  ${RED}✗${NC} DATABASE_URL 使用了错误的用户名 (fde_user)"
    ERRORS=$((ERRORS + 1))
else
    echo -e "  ${YELLOW}⚠${NC} DATABASE_URL 凭证未验证"
    WARNINGS=$((WARNINGS + 1))
fi
echo ""

# 5. 检查 AI Orchestrator 连接
echo "🤖 5. 检查 AI Orchestrator..."
if curl -s http://localhost:8090/health > /dev/null 2>&1; then
    echo -e "  ${GREEN}✓${NC} AI Orchestrator 健康检查通过"
else
    echo -e "  ${RED}✗${NC} AI Orchestrator 无法访问"
    ERRORS=$((ERRORS + 1))
fi

if curl -s -X POST http://localhost:8090/ai/chat \
    -H "Content-Type: application/json" \
    -d '{"assistantId": "chat", "message": "test", "userId": 1}' 2>&1 | grep -q "data:"; then
    echo -e "  ${GREEN}✓${NC} AI Orchestrator 对话接口正常"
else
    echo -e "  ${RED}✗${NC} AI Orchestrator 对话接口异常"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# 6. 检查 API 服务健康
echo "🌐 6. 检查 API 服务..."
if curl -s http://localhost:8080/health > /dev/null 2>&1; then
    echo -e "  ${GREEN}✓${NC} API 健康检查通过"
else
    echo -e "  ${RED}✗${NC} API 服务无法访问"
    ERRORS=$((ERRORS + 1))
fi

# 测试登录接口
LOGIN_RESPONSE=$(curl -s -X POST http://localhost:8080/api/v1/auth/login \
    -H "Content-Type: application/json" \
    -d '{"username": "admin", "password": "admin123"}')

if echo "$LOGIN_RESPONSE" | grep -q "accessToken"; then
    echo -e "  ${GREEN}✓${NC} 登录接口正常"
    TOKEN=$(echo "$LOGIN_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['accessToken'])" 2>/dev/null || echo "")
else
    echo -e "  ${RED}✗${NC} 登录接口异常"
    echo "  响应: $LOGIN_RESPONSE"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# 7. 检查 AI 对话接口
if [ -n "$TOKEN" ]; then
    echo "💬 7. 检查 AI 对话接口..."
    COPILOT_RESPONSE=$(curl -s -N -X POST http://localhost:8080/api/v1/copilot/chat \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $TOKEN" \
        -d '{"assistantId": "chat", "message": "测试", "sessionId": "test-session"}' 2>&1 | head -1)
    
    if echo "$COPILOT_RESPONSE" | grep -q "data:"; then
        echo -e "  ${GREEN}✓${NC} AI 对话接口正常"
    else
        echo -e "  ${RED}✗${NC} AI 对话接口异常"
        echo "  响应: $COPILOT_RESPONSE"
        ERRORS=$((ERRORS + 1))
    fi
    echo ""
fi

# 8. 检查前端开发服务器
echo "🖥️  8. 检查前端服务..."
if curl -s http://localhost:5173/ > /dev/null 2>&1; then
    echo -e "  ${GREEN}✓${NC} 前端服务运行在 5173 端口"
else
    echo -e "  ${RED}✗${NC} 前端服务未运行在 5173 端口"
    echo "  提示: cd workspace/web && npm run dev"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# 总结
echo "======================================"
echo "  检查结果汇总"
echo "======================================"
if [ $ERRORS -gt 0 ]; then
    echo -e "${RED}❌ 发现 $ERRORS 个错误，请先修复后再部署${NC}"
    exit 1
elif [ $WARNINGS -gt 0 ]; then
    echo -e "${YELLOW}⚠️  发现 $WARNINGS 个警告，可以部署但建议检查${NC}"
    exit 0
else
    echo -e "${GREEN}✅ 所有检查通过，可以安全部署！${NC}"
    exit 0
fi
