<!--
 * @Author: 刘霁雯
 * @Date: 2019-12-02 11:31:12
 * @LastEditTime: 2019-12-02 11:31:55
 * @LastEditors: Please set LastEditors
 * @Description: 图标
 * @FilePath: \taodongdong\components\SvgIcon\pro.vue
 -->
<template>
  <svg
    :class="svgClass"
    aria-hidden="true">
    <use :xlink:href="iconName"></use>
  </svg>
</template>

<script>
export default {
  name: 'svg-icon',
  props: {
    iconClass: {
      type: String,
      required: true
    },
    className: {
      type: String,
      default: ''
    }
  },
  computed: {
    iconName () {
      return `#icon-${this.iconClass}`
    },
    svgClass () {
      if (this.className) {
        return 'svg-icon' + this.className
      } else {
        return 'svg-icon'
      }
    }
  }
}
</script>

<style scoped>
  .svg-icon {
    width: 1em;
    height: 1em;
    vertical-align: -0.15em;
    fill: currentColor;
    overflow: hidden;
  }
</style>
