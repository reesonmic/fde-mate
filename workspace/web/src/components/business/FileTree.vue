<script setup lang="ts">
import { ref } from 'vue'
import { Tree } from 'ant-design-vue'

interface TreeNode {
  key: string
  title: string
  children?: TreeNode[]
  isLeaf?: boolean
}

interface Props {
  data: TreeNode[]
}

const props = defineProps<Props>()

const expandedKeys = ref<string[]>([])
const selectedKeys = ref<string[]>([])

const handleSelect = (keys: string[]) => {
  selectedKeys.value = keys
}
</script>

<template>
  <div class="file-tree">
    <Tree
      :treeData="data"
      :expandedKeys="expandedKeys"
      :selectedKeys="selectedKeys"
      @select="handleSelect"
      class="file-tree-component"
    />
  </div>
</template>

<style scoped>
.file-tree {
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: 12px;
}

.file-tree-component {
  background: transparent;
}
</style>