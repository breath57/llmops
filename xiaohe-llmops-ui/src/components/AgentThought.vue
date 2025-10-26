<script setup lang="ts">
import { type PropType, ref } from 'vue'
import { QueueEvent } from '@/config'
import MessagePreviewModal from './MessagePreviewModal.vue'
import MessageHoverPreview from './MessageHoverPreview.vue'

// 1.定义自定义组件所需数据
const props = defineProps({
  loading: { type: Boolean, default: false, required: true },
  agent_thoughts: {
    type: Array as PropType<Record<string, any>[]>,
    default: () => [],
    required: true,
  },
})
const visible = ref(false)

// 消息预览相关状态
const previewModalVisible = ref(false)
const previewContent = ref('')
const previewTitle = ref('')

// 悬停预览相关状态
const hoverPreviewVisible = ref(false)
const hoverPreviewContent = ref('')
const hoverPreviewPosition = ref({ x: 0, y: 0 })
let hoverTimer: number | null = null

// 处理消息内容点击预览
const handleContentClick = (content: string, eventType: string) => {
  if (!content || content === '-') return
  
  previewContent.value = content
  previewTitle.value = getEventTitle(eventType)
  previewModalVisible.value = true
}

// 获取事件类型对应的标题
const getEventTitle = (eventType: string) => {
  const titleMap: Record<string, string> = {
    [QueueEvent.longTermMemoryRecall]: '长期记忆召回',
    [QueueEvent.agentThought]: '智能体推理',
    [QueueEvent.datasetRetrieval]: '搜索知识库',
    [QueueEvent.agentAction]: '调用工具',
    [QueueEvent.agentMessage]: '智能体消息',
  }
  return titleMap[eventType] || '消息内容预览'
}

// 处理鼠标悬停进入
const handleMouseEnter = (event: MouseEvent, content: string) => {
  if (!content || content === '-') return
  
  // 清除之前的定时器
  if (hoverTimer) {
    window.clearTimeout(hoverTimer)
  }
  
  // 设置延迟显示，避免鼠标快速移动时频繁显示
  hoverTimer = window.setTimeout(() => {
    hoverPreviewContent.value = content
    hoverPreviewPosition.value = { x: event.clientX, y: event.clientY }
    hoverPreviewVisible.value = true
  }, 300) // 300ms延迟
}

// 处理鼠标悬停离开
const handleMouseLeave = () => {
  // 清除定时器
  if (hoverTimer) {
    window.clearTimeout(hoverTimer)
    hoverTimer = null
  }
  
  // 延迟隐藏，给用户时间移动到预览框
  window.setTimeout(() => {
    hoverPreviewVisible.value = false
  }, 100)
}

// 处理鼠标移动，更新预览框位置
const handleMouseMove = (event: MouseEvent) => {
  if (hoverPreviewVisible.value) {
    hoverPreviewPosition.value = { x: event.clientX, y: event.clientY }
  }
}
</script>

<template>
  <!-- 智能体推理步骤 -->
  <div :class="`flex flex-col rounded-2xl border ${visible ? 'w-[320px]' : 'w-[180px]'}`">
    <div
      :class="`flex items-center justify-between h-10 rounded-2xl bg-gray-100 px-4 text-gray-700 cursor-pointer w-auto ${visible ? 'rounded-bl-none rounded-br-none' : ''}`"
      @click="visible = !visible"
    >
      <!-- 左侧图标与标题 -->
      <div class="flex items-center gap-2">
        <icon-list />
        {{ visible ? '隐藏' : '显示' }}运行流程
      </div>
      <!-- 右侧图标 -->
      <div class="">
        <template v-if="props.loading">
          <icon-loading />
        </template>
        <template v-else>
          <icon-up v-if="visible" />
          <icon-down v-else />
        </template>
      </div>
    </div>
    <!-- 底部内容 -->
    <a-collapse class="agent-thought" v-if="visible" destroy-on-hide :bordered="false">
      <a-collapse-item
        v-for="agent_thought in props.agent_thoughts.filter((item: any) =>
          [
            QueueEvent.longTermMemoryRecall,
            QueueEvent.agentThought,
            QueueEvent.datasetRetrieval,
            QueueEvent.agentAction,
            QueueEvent.agentMessage,
          ].includes(item.event),
        )"
        :key="agent_thought.id"
      >
        <template #expand-icon>
          <icon-file v-if="agent_thought.event === QueueEvent.longTermMemoryRecall" />
          <icon-language v-else-if="agent_thought.event === QueueEvent.agentThought" />
          <icon-storage v-else-if="agent_thought.event === QueueEvent.datasetRetrieval" />
          <icon-tool v-else-if="agent_thought.event === QueueEvent.agentAction" />
          <icon-message v-else-if="agent_thought.event === QueueEvent.agentMessage" />
        </template>
        <template #header>
          <div class="text-gray-700" v-if="agent_thought.event === QueueEvent.longTermMemoryRecall">
            长期记忆召回
          </div>
          <div class="text-gray-700" v-if="agent_thought.event === QueueEvent.agentThought">
            智能体推理
          </div>
          <div class="text-gray-700" v-if="agent_thought.event === QueueEvent.datasetRetrieval">
            搜索知识库
          </div>
          <div class="text-gray-700" v-if="agent_thought.event === QueueEvent.agentAction">
            调用工具
          </div>
          <div class="text-gray-700" v-if="agent_thought.event === QueueEvent.agentMessage">
            智能体消息
          </div>
        </template>
        <template #extra>
          <div class="text-gray-500">{{ agent_thought.latency.toFixed(2) }}s</div>
        </template>
        <div
          v-if="['agent_thought', 'agent_message'].includes(agent_thought.event)"
          class="text-xs text-gray-500 line-clamp-4 break-all cursor-pointer hover:bg-gray-50 rounded p-1 transition-colors"
          @click="handleContentClick(agent_thought.thought || '-', agent_thought.event)"
          @mouseenter="(event) => handleMouseEnter(event, agent_thought.thought || '-')"
          @mouseleave="handleMouseLeave"
          @mousemove="handleMouseMove"
          :title="agent_thought.thought && agent_thought.thought !== '-' ? '点击查看完整内容，悬停预览' : ''"
        >
          {{ agent_thought.thought || '-' }}
        </div>
        <div 
          v-else 
          class="text-xs text-gray-500 line-clamp-4 break-all cursor-pointer hover:bg-gray-50 rounded p-1 transition-colors"
          @click="handleContentClick(agent_thought.observation || '-', agent_thought.event)"
          @mouseenter="(event) => handleMouseEnter(event, agent_thought.observation || '-')"
          @mouseleave="handleMouseLeave"
          @mousemove="handleMouseMove"
          :title="agent_thought.observation && agent_thought.observation !== '-' ? '点击查看完整内容，悬停预览' : ''"
        >
          {{ agent_thought.observation || '-' }}
        </div>
      </a-collapse-item>
    </a-collapse>
  </div>
  
  <!-- 消息内容预览模态框 -->
  <message-preview-modal
    v-model:visible="previewModalVisible"
    :title="previewTitle"
    :content="previewContent"
  />
  
  <!-- 鼠标悬停预览 -->
  <message-hover-preview
    :visible="hoverPreviewVisible"
    :content="hoverPreviewContent"
    :position="hoverPreviewPosition"
  />
</template>

<style>
.agent-thought {
  .arco-collapse-item-content {
    padding: 0 16px;
  }
}
</style>
