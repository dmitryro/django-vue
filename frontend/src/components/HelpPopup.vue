<template>
<q-modal
  v-model="value"
  maximized
  :content-css="{padding: '50px'}"
>
  <q-modal-layout>
    <q-toolbar slot="header">
      
      <q-toolbar-title>
        HELP
      </q-toolbar-title>
 
    </q-toolbar>

<q-btn
                style="width:160px"
                color="primary"
                flat
                v-close-overlay
            >
                close
            </q-btn>

    <div class="layout-padding">
    </div>
  </q-modal-layout>
</q-modal>
</template>

<script>
import {
  QModal,
  QModalLayout,
  QBtn,
  QIcon,
  QToolbar,
  QToolbarTitle,
  CloseOverlay
} from "quasar-framework";

export default {
  props: ["value"],
  methods: {
    close() {
      this.isOpened = false;
    }
  },
  data() {
    return {
      isOpened: false
    };
  },
  components: {
    CloseOverlay,
    QModal,
    QModalLayout,
    QBtn,
    QToolbar,
    QIcon,
    QToolbarTitle
  }
};
</script>

