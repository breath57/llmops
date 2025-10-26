<script setup lang="ts">
import { computed, ref, nextTick } from 'vue'

// 定义组件属性
const props = defineProps({
  visible: { type: Boolean, default: false, required: true },
  content: { type: String, default: '', required: true },
  position: { 
    type: Object as () => { x: number; y: number }, 
    default: () => ({ x: 0, y: 0 }), 
    required: false 
  },
})

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

// 计算预览框的样式
const previewStyle = computed(() => {
  if (!props.visible) return { display: 'none' }
  
  const { x, y } = props.position
  
  // 确保预览框不会超出视窗边界
  const maxWidth = 400
  const maxHeight = 300
  
  let left = x + 10 // 鼠标右侧10px
  let top = y + 10  // 鼠标下方10px
  
  // 检查是否会超出右边界
  if (left + maxWidth > window.innerWidth) {
    left = x - maxWidth - 10 // 显示在鼠标左侧
  }
  
  // 检查是否会超出下边界
  if (top + maxHeight > window.innerHeight) {
    top = y - maxHeight - 10 // 显示在鼠标上方
  }
  
  return {
    position: 'fixed' as const,
    left: `${Math.max(10, left)}px`,
    top: `${Math.max(10, top)}px`,
    maxWidth: `${maxWidth}px`,
    maxHeight: `${maxHeight}px`,
    zIndex: 9999,
  }
})

// 限制显示的内容长度，避免预览框过大
const truncatedContent = computed(() => {
  const content = processedContent.value
  const maxLength = 500 // 最大显示500个字符
  
  if (content.length <= maxLength) {
    return content
  }
  
  return content.substring(0, maxLength) + '...\n\n[点击查看完整内容]'
})
</script>

<template>
  <div
    v-if="visible"
    :style="previewStyle"
    class="message-hover-preview bg-white border border-gray-300 rounded-lg shadow-lg p-3 overflow-hidden"
  >
    <div class="text-xs text-gray-600 mb-2 font-medium">内容预览</div>
    <div class="overflow-y-auto max-h-60">
      <pre class="whitespace-pre-wrap text-xs text-gray-700 font-mono leading-relaxed">{{ truncatedContent }}</pre>
    </div>
  </div>
</template>

<style scoped>
.message-hover-preview {
  /* 确保长文本能够正确换行 */
  word-wrap: break-word;
  word-break: break-all;
  /* 添加一些视觉效果 */
  backdrop-filter: blur(10px);
  background-color: rgba(255, 255, 255, 0.95);
}

/* 自定义滚动条样式 */
.message-hover-preview ::-webkit-scrollbar {
  width: 4px;
}

.message-hover-preview ::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 2px;
}

.message-hover-preview ::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 2px;
}

.message-hover-preview ::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>
