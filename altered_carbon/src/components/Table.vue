<template>
  <CCard>
    <CCardHeader>
      <slot name="header">
        <CIcon name="cil-grid" /> {{ caption }}
      </slot>
    </CCardHeader>
    <CCardBody>
      <CDataTable
        :clickable-rows="clickable"
        :hover="hover"
        :striped="striped"
        :bordered="bordered"
        :small="small"
        :fixed="fixed"
        :items="items"
        :fields="fields"
        :items-per-page="small ? 15 : 10"
        :dark="dark"
        pagination
        @row-clicked="rowClick">
        <template #status="{item}">
          <td>
            <CBadge :color="getBadge(item.status)">
              {{ item.status }}
            </CBadge>
          </td>
        </template>
      </CDataTable>
    </CCardBody>
  </CCard>
</template>

<script>
export default {
  name: 'Table',
  props: {
    items: {
      type: Array,
      default () {
        return [];
      }
    },
    fields: {
      type: Array,
      default () {
        return [];
      }
    },
    caption: {
      type: String,
      default: 'Table'
    },
    hover: Boolean,
    striped: Boolean,
    bordered: Boolean,
    small: Boolean,
    fixed: Boolean,
    dark: Boolean,
    clickable: Boolean,
  },
  methods: {
    getBadge (status) {
      return status === 'Active' ? 'success'
        : status === 'Inactive' ? 'secondary'
          : status === 'Pending' ? 'warning'
            : status === 'Banned' ? 'danger' : 'primary';
    },
    rowClick(payload) {
      this.$emit('row-clicked', payload);
    }
  }
};
</script>
