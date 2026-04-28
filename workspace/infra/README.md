# infra · 基础设施

Docker / Kubernetes / Helm / Nginx / 监控配置。

详细设计：[05-部署运维详细设计.md](../../docs/detail-design/05-部署运维详细设计.md)

## 目录

```
infra/
├── docker-compose/    # 本地开发一键启动
│   ├── docker-compose.yml          # 全栈
│   └── docker-compose.deps.yml     # 仅依赖（MySQL/Redis/ES/Milvus）
├── k8s/               # Kustomize 风格 K8s 资源
│   ├── base/
│   └── overlays/      # test/staging/prod
├── helm/              # Helm Chart（与 k8s/ 二选一）
├── nginx/             # Nginx 配置（前端静态 + SSE 转发）
├── grafana/           # Dashboard JSON
├── prometheus/        # 告警规则
├── argocd/            # ArgoCD Application
└── terraform/         # 云资源（可选）
```

## 常用命令

```bash
# 本地拉起依赖
cd docker-compose && docker-compose -f docker-compose.deps.yml up -d

# 应用 K8s 资源到 test 环境
kustomize build k8s/overlays/test | kubectl apply -f -

# Helm 升级
helm upgrade --install fde helm/fde-workspace -f helm/fde-workspace/values-staging.yaml
```

## 命名规范

K8s 资源统一前缀 `fde-`：
- `fde-web` / `fde-api` / `fde-ai` / `fde-celery` / `fde-celery-beat`

完整命名约定见 [00-目录结构设计 §十](../../docs/detail-design/00-目录结构设计.md)。
