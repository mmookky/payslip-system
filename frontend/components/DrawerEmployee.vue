<template>
  <v-navigation-drawer
    v-model:rail="rail"
    permanent
    expand-on-hover
    rail
    color="deep_blue"
  >
    <v-list>
      <v-list-item
        prepend-icon="mdi-account"
        subtitle="Payslip System"
        title="Employee"
      />
    </v-list>

    <v-divider />
    <v-list nav>
      <v-list-item
        prepend-icon="mdi-file-document-multiple"
        title="My Payslips"
        to="/employee/payslip"
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

    