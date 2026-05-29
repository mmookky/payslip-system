<template>
  <v-navigation-drawer
    v-model:rail="rail"
    permanent
    expand-on-hover
    rail
    color="primary"
  >
    <v-list>
      <v-list-item
        prepend-icon="mdi-shield-account"
        title="Admin / HR"
        subtitle="Payslip System"
      ></v-list-item>
    </v-list>
    <v-divider />
    <v-list nav>
      <v-list-item
        prepend-icon="mdi-upload"
        title="Upload Payslip"
        to="/admin/upload"
        rounded="lg"
      />
      <v-list-item
        prepend-icon="mdi-table"
        title="Payslip Result"
        to="/admin/result"
        rounded="lg"
      />
      <v-list-item
        prepend-icon="mdi-history"
        title="Upload History"
        to="/admin/history"
        rounded="lg"
      />
    </v-list>
    <template #append>
      <div class="pa-3">
        <v-btn block variant="outlined" color="white" @click="logout">
          <v-icon>mdi-logout</v-icon>
          <span v-show="!rail" class="ml-2"> Logout </span>
        </v-btn>
      </div>
    </template>
  </v-navigation-drawer>
</template>
    
<script setup>
const auth = useAuthStore();
const router = useRouter();
const rail = ref(true);

const logout = () => {
  auth.logout();
  router.push("/");
};
</script>