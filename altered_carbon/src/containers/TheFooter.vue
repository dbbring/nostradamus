<template>
  <CFooter
    :fixed="false"
    class="bg-light">
    <div>
      Altered Carbon
      <span class="px-4">|</span>
      Carbon Black
      <span class="px-4">|</span>
      Nostradamus
    </div>
    <div class="ml-auto">
      <span class="ml-1">&copy; {{new Date().getFullYear()}} Derek Bringewatt</span>
    </div>
  </CFooter>
</template>

<script>
export default {
  name: 'TheFooter'
}
</script>
