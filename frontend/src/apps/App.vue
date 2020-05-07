<template>
	<div id="q-app">
		<q-layout v-model="sides" view="hHr LpR lFf" :right-breakpoint="1100">
			
			<q-toolbar slot="header" color="primary">
				<q-btn flat @click="sides.left = !sides.left">
					<q-icon name="menu" />
				</q-btn>
				<q-toolbar-title>
					Quasar <small><sup>v{{$q.version}}</sup></small>
					<span slot="subtitle">
						VueJS UI Framework
					</span>
				</q-toolbar-title>
			</q-toolbar>

			<q-toolbar slot="header" color="secondary">
				<q-btn flat @click="sides.left = !sides.left">
					<q-icon name="menu" />
				</q-btn>
				<q-toolbar-title>
					Duplicated Quasar <small><sup>v{{$q.version}}</sup></small>
					<span slot="subtitle">
						VueJS UI Framework
					</span>
				</q-toolbar-title>
			</q-toolbar>

			<h1>Hello World!</h1>

<help-popup
      v-model="showHelp"
      @close="showHelp=false"
    />

<q-btn
                style="width:160px"
                color="primary"
                flat
                @click="showHelp=true"
            >
                Help
            </q-btn>
						
		</q-layout>
	</div>
</template>

<script>
import {
  QLayout,
  QToolbar,
  QToolbarTitle,
  QIcon,
  QBtn,
  QScrollArea,
  QList,
  QListHeader,
  QSideLink,
  QItemMain,
  QItemSide
} from "quasar-framework";
import SidebarMenuItem from "./components/SidebarMenuItem";
import HelpPopup from "./components/HelpPopup";
export default {
  name: "app",
  components: {
    QLayout,
    QToolbar,
    QToolbarTitle,
    QIcon,
    QBtn,
    QScrollArea,
    QList,
    QListHeader,
    QSideLink,
    QItemMain,
    QItemSide,
    SidebarMenuItem,
    HelpPopup
  },
  data: () => ({
    showHelp: false,
    pages: [{ path: ["Hello"] }],
    sides: {
      left: true,
      right: false
    }
  })
};
</script>

