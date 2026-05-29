<template>
  <v-app>
    <v-main class="bg-deep_blue">
      <v-container class="fill-height" fluid>
        <v-row justify="center" align="center">
          <v-col cols="12" sm="6" md="4">
            <v-card rounded="lg" elevation="3" class="pa-6">
              <!-- Header -->
              <div class="text-center mb-8">
                <v-avatar color="primary" size="64" class="mb-4">
                  <span class="text-h5 font-weight-bold text-white">A</span>
                </v-avatar>
                <h1 class="text-h5 font-weight-bold">Payroll system</h1>
                <p class="text-body-2 text-medium-emphasis mt-1">
                  Self-Service Payslip System
                </p>
              </div>

              <!-- Buttons -->
              <v-btn
                block
                color="primary"
                size="large"
                rounded="lg"
                class="mb-3 text-none"
                to="/admin/login"
              >
                <v-icon start>mdi-shield-account</v-icon>
                Log-in Admin / HR
              </v-btn>

              <v-btn
                block
                color="secondary"
                size="large"
                rounded="lg"
                variant="outlined"
                to="/employee/login"
                class="text-none"
              >
                <v-icon start>mdi-account</v-icon>
                Log-in Employee
              </v-btn>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
definePageMeta({
  middleware: "guest",
});
</script>