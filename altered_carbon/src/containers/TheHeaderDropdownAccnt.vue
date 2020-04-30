<template>
  <CDropdown
    inNav
    class="c-header-nav-items bg-dark"
    placement="bottom-end"
    add-menu-classes="pt-0">
    <template #toggler>
      <CHeaderNavLink>
        <div class="c-avatar">
          <img
            src="img/ac_fire_cropped.jpg"
            class="c-avatar-img "/>
        </div>
      </CHeaderNavLink>
    </template>
    <CDropdownHeader tag="div" class="text-center" color="light">
      <strong>Account</strong>
    </CDropdownHeader>
    <CDropdownItem class="bg-dark text-white">
      <CIcon name="cil-comment-square" /> Comments
      <CBadge color="warning" class="ml-auto">{{ itemsCount }}</CBadge>
    </CDropdownItem>
    <CDropdownHeader
      tag="div"
      class="text-center"
      color="light">
      <strong>Settings</strong>
    </CDropdownHeader>
    <CDropdownItem class="bg-dark text-white">
      <CIcon name="cil-settings" /> Settings
    </CDropdownItem>
    <CDropdownItem class="bg-dark text-white">
      <CIcon name="cil-settings" /> Nostradamus Settings
    </CDropdownItem>
    <CDropdownItem class="bg-dark text-white">
      <CIcon name="cil-file" /> Projects
      <CBadge color="primary" class="ml-auto">{{ itemsCount }}</CBadge>
    </CDropdownItem>
  </CDropdown>
</template>

<script>
export default {
  name: 'TheHeaderDropdownAccnt',
  data () {
    return { 
      itemsCount: 42
    }
  }
}
</script>

<style scoped>
  .c-icon {
    margin-right: 0.3rem;
  }
</style>