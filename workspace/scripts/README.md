# scripts · 一键脚本

```
scripts/
├── dev/          # 本地开发：start-all / stop-all / reset-db / seed
├── test/         # 测试：unit / integration / perf
├── release/      # 发布：bump-version / changelog
├── data/         # 数据初始化：导入案例/SOP/重建 RAG 索引
└── ci/           # CI 用：lint / check-openapi-sync
```

## 常用脚本

```bash
# 一键启动全部服务
./dev/start-all.sh

# 重置数据库 + 灌入种子数据
./dev/reset-db.sh

# 导入 86 个最佳实践案例
python data/import-best-practices.py

# 重建全量 RAG 索引
python data/rebuild-rag-index.py
```

## 编写规范

- Bash 脚本统一加 `set -euo pipefail`
- Python 脚本统一加 shebang `#!/usr/bin/env python3` + UTF-8 编码声明
- 所有脚本顶部必须有用途、参数说明、示例
