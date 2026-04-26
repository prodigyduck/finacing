<template>
  <v-app>
    <v-navigation-drawer permanent :width="220" color="surface" border="r">
      <div class="d-flex align-center ga-3 pa-4 mb-6">
        <v-avatar size="36" color="primary" rounded="lg">
          <span class="text-white font-weight-bold text-body-1">W</span>
        </v-avatar>
        <span class="text-h6 font-weight-bold">Financing</span>
      </div>
      <v-list density="compact" nav>
        <v-list-item to="/" prepend-icon="mdi-chart-line" title="Dashboard" exact />
        <v-list-item to="/raw-data" prepend-icon="mdi-table-edit" title="Raw Data" exact />
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>
