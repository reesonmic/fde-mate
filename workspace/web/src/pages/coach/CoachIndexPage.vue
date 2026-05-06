<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Row, Col, Card, Input, Tag, Select, Spin, Empty, Statistic } from 'ant-design-vue'
import { BookOutlined, RocketOutlined } from '@ant-design/icons-vue'
import { useRouter } from 'vue-router'
import { coachApi } from '@apis/modules/coach'

const router = useRouter()
const loading = ref(false)
import type { BestPracticeDTO, SopDTO, LearningPathDTO } from '@/types/business'

interface RecommendationsDTO {
  practices?: BestPracticeDTO[]
  sops?: SopDTO[]
  paths?: LearningPathDTO[]
}

const recommendations = ref<RecommendationsDTO | null>(null)

const sections = [
  { key: 'practices', title: '最佳实践', icon: BookOutlined, route: '/coach/best-practices', desc: '实战案例库' },
  { key: 'sops', title: 'SOP库', icon: RocketOutlined, route: '/coach/sops', desc: '标准操作流程' },
  { key: 'learning', title: '学习路径', icon: BookOutlined, route: '/coach/learning-path', desc: '个性化成长' },
]

const stats = computed(() => {
  if (!recommendations.value) return null
  return {
    practiceCount: recommendations.value.practices?.length ?? 0,
    sopCount: recommendations.value.sops?.length ?? 0,
    pathCount: recommendations.value.paths?.length ?? 0,
  }
})

onMounted(async () => {
  loading.value = true
  try {
    recommendations.value = await coachApi.getRecommendations()
  } catch (e) {
    console.error('Failed to load recommendations', e)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="coach-index-page">
    <Spin :spinning="loading">
      <div class="page-header">
        <h2>FDE教练</h2>
        <p>实战经验与标准流程，助力高效交付</p>
      </div>

      <!-- Entry Cards -->
      <Row :gutter="16" class="entry-cards">
        <Col v-for="section in sections" :key="section.key" :span="8">
          <Card hoverable class="entry-card" @click="router.push(section.route)">
            <div class="entry-icon">
              <component :is="section.icon" />
            </div>
            <h3>{{ section.title }}</h3>
            <p>{{ section.desc }}</p>
          </Card>
        </Col>
      </Row>

      <!-- Recommendations -->
      <Card title="为你推荐" :bordered="false" v-if="recommendations">
        <Row :gutter="16">
          <Col :span="8">
            <h4>最新案例</h4>
            <div v-if="recommendations.practices?.length" class="recommend-list">
              <div
                v-for="item in recommendations.practices.slice(0, 3)"
                :key="item.id"
                class="recommend-item"
                @click="router.push(`/coach/best-practices/${item.id}`)"
              >
                <Tag color="blue">{{ item.category }}</Tag>
                <span>{{ item.title }}</span>
              </div>
            </div>
            <Empty v-else description="暂无推荐案例" :image="Empty.PRESENTED_IMAGE_SIMPLE" />
          </Col>
          <Col :span="8">
            <h4>热门SOP</h4>
            <div v-if="recommendations.sops?.length" class="recommend-list">
              <div
                v-for="item in recommendations.sops.slice(0, 3)"
                :key="item.id"
                class="recommend-item"
                @click="router.push(`/coach/sops/${item.id}`)"
              >
                <Tag color="green">v{{ item.version }}</Tag>
                <span>{{ item.title }}</span>
              </div>
            </div>
            <Empty v-else description="暂无推荐SOP" :image="Empty.PRESENTED_IMAGE_SIMPLE" />
          </Col>
          <Col :span="8">
            <h4>学习路径</h4>
            <div v-if="recommendations.paths?.length" class="recommend-list">
              <div
                v-for="item in recommendations.paths.slice(0, 3)"
                :key="item.id"
                class="recommend-item"
                @click="router.push(`/coach/learning-path/${item.id}`)"
              >
                <Tag color="purple">{{ item.difficulty }}</Tag>
                <span>{{ item.name }}</span>
              </div>
            </div>
            <Empty v-else description="暂无推荐路径" :image="Empty.PRESENTED_IMAGE_SIMPLE" />
          </Col>
        </Row>
      </Card>

      <!-- Stats -->
      <Row :gutter="16" class="stats-row" v-if="stats">
        <Col :span="8">
          <Card :bordered="false" class="stat-card">
            <Statistic title="最佳实践" :value="stats.practiceCount" suffix="篇" />
          </Card>
        </Col>
        <Col :span="8">
          <Card :bordered="false" class="stat-card">
            <Statistic title="标准流程" :value="stats.sopCount" suffix="个" />
          </Card>
        </Col>
        <Col :span="8">
          <Card :bordered="false" class="stat-card">
            <Statistic title="学习路径" :value="stats.pathCount" suffix="条" />
          </Card>
        </Col>
      </Row>
    </Spin>
  </div>
</template>

<style scoped>
.coach-index-page {
  padding: 24px;
}

.page-header {
  margin-bottom: 32px;
}

.page-header h2 {
  margin: 0 0 8px;
}

.page-header p {
  margin: 0;
  color: var(--color-text-secondary, #666);
}

.entry-cards {
  margin-bottom: 24px;
}

.entry-card {
  text-align: center;
  cursor: pointer;
}

.entry-icon {
  font-size: 48px;
  color: #1677ff;
  margin-bottom: 12px;
}

.entry-card h3 {
  margin: 0 0 8px;
}

.entry-card p {
  margin: 0;
  color: var(--color-text-secondary, #666);
}

.recommend-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.recommend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px;
  border-radius: 4px;
  cursor: pointer;
}

.recommend-item:hover {
  background: #f5f5f5;
}

.stats-row {
  margin-top: 24px;
}

.stat-card {
  text-align: center;
}

.stat-card :deep(.ant-statistic-title) {
  font-size: 14px;
  color: var(--color-text-secondary, #666);
}
</style>
