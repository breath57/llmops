<script setup lang="ts">
import { computed } from 'vue'

// 定义组件属性
const props = defineProps({
  visible: { type: Boolean, default: false, required: true },
  title: { type: String, default: '消息内容预览', required: false },
  content: { type: String, default: '', required: true },
})

// 定义事件
const emits = defineEmits(['update:visible'])

// 处理关闭模态框
const handleCancel = () => {
  emits('update:visible', false)
}

// 处理转义字符，将转义字符转换为实际字符
const processedContent = computed(() => {
  if (!props.content) return ''
  
  return props.content
    .replace(/\\n/g, '\n')           // 换行符
    .replace(/\\t/g, '\t')           // 制表符
    .replace(/\\r/g, '\r')           // 回车符
    .replace(/\\"/g, '"')            // 双引号
    .replace(/\\'/g, "'")            // 单引号
    .replace(/\\\\/g, '\\')          // 反斜杠
    .replace(/\\b/g, '\b')           // 退格符
    .replace(/\\f/g, '\f')           // 换页符
    .replace(/\\v/g, '\v')           // 垂直制表符
})
</script>

<template>
  <a-modal
    :visible="props.visible"
    :width="800"
    hide-title
    :footer="false"
    modal-class="rounded-xl"
    @cancel="handleCancel"
  >
    <!-- 顶部标题 -->
    <div class="flex items-center justify-between mb-4">
      <div class="text-lg font-bold text-gray-700">{{ props.title }}</div>
      <a-button type="text" class="!text-gray-700" size="small" @click="handleCancel">
        <template #icon>
          <icon-close />
        </template>
      </a-button>
    </div>
    
    <!-- 内容区域 -->
    <div class="max-h-[60vh] overflow-y-auto">
      <div class="bg-gray-50 rounded-lg p-4 border">
        <pre class="whitespace-pre-wrap text-sm text-gray-700 font-mono leading-relaxed">{{ processedContent }}</pre>
      </div>
    </div>
    
    <!-- 底部操作按钮 -->
    <div class="flex justify-end mt-4">
      <a-button class="rounded-lg" @click="handleCancel">关闭</a-button>
    </div>
  </a-modal>
</template>

<style scoped>
/* 确保长文本能够正确换行 */
pre {
  word-wrap: break-word;
  word-break: break-all;
}
</style>
