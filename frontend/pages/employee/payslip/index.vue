<template>
  <v-app class="bg-sky">
    <DrawerEmployee />
    <v-main>
      <v-container class="pa-6">
        <h1 class="text-h5 font-weight-bold mb-6">My Payslips</h1>

        <!-- Filter -->
        <v-card rounded="lg" elevation="2" class="pa-4 mb-6">
          <v-row align="center">
            <v-col cols="12" sm="4" md="3">
              <v-select
                v-model="filter.month"
                :items="[
                  { label: 'All Months', value: null },
                  ...monthsList.list,
                ]"
                item-title="label"
                item-value="value"
                label="Month"
                variant="outlined"
                rounded="lg"
                density="compact"
                hide-details
                clearable
              />
            </v-col>
            <v-col cols="12" sm="4" md="3">
              <v-select
                v-model="filter.year"
                :items="[{ label: 'All Years', value: null }, ...yearItems]"
                item-title="label"
                item-value="value"
                label="Year"
                variant="outlined"
                rounded="lg"
                density="compact"
                hide-details
                clearable
              />
            </v-col>
          </v-row>
        </v-card>

        <!-- Loading -->
        <v-row v-if="loading">
          <v-col v-for="i in 3" :key="i" cols="12" sm="6" md="4">
            <v-skeleton-loader type="card" rounded="lg" />
          </v-col>
        </v-row>

        <!-- No data -->
        <v-card
          v-else-if="filteredPayslips.length === 0"
          rounded="lg"
          elevation="2"
          class="pa-8 text-center"
        >
          <v-icon size="64" color="grey-lighten-1" class="mb-4"
            >mdi-file-document-off</v-icon
          >
          <p class="text-h6 text-medium-emphasis">No payslip found</p>
        </v-card>

        <!-- Payslip list -->
        <v-row v-else>
          <v-col
            v-for="slip in filteredPayslips"
            :key="slip.id"
            cols="12"
            sm="6"
            md="4"
          >
            <v-card
              rounded="lg"
              elevation="2"
              hover
              @click="router.push(`/employee/payslip/${slip.id}`)"
            >
              <v-card-item>
                <template #prepend>
                  <v-avatar color="secondary" variant="tonal">
                    <v-icon>mdi-file-document</v-icon>
                  </v-avatar>
                </template>
                <v-card-title
                  >{{ monthName(slip.month) }} {{ slip.year }}</v-card-title
                >
                <v-card-subtitle>Payslip</v-card-subtitle>
              </v-card-item>
              <v-divider />
              <v-card-text>
                <div class="d-flex justify-space-between align-center">
                  <span class="text-body-2 text-medium-emphasis">Net Pay</span>
                  <span class="text-h6 font-weight-bold text-secondary">
                    ฿{{ formatNumber(slip.net_pay) }}
                  </span>
                </div>
              </v-card-text>
              <v-card-actions>
                <v-spacer />
                <v-btn
                  color="secondary"
                  variant="text"
                  :to="`/employee/payslip/${slip.id}`"
                  class="text-none"
                >
                  View Detail
                  <v-icon end>mdi-chevron-right</v-icon>
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
definePageMeta({ middleware: "auth" });

const { api } = useApi();
const router = useRouter();

const loading = ref(false);
const payslips = ref([]);

const currentYear = new Date().getFullYear();

const yearItems = Array.from({ length: 5 }, (_, i) => ({
  label: String(currentYear - i),
  value: currentYear - i,
}));

const filter = reactive({ month: null, year: null });

const formatNumber = (n) =>
  Number(n).toLocaleString("en-US", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });

const filteredPayslips = computed(() => {
  return payslips.value.filter((slip) => {
    if (filter.month && slip.month !== filter.month) return false;
    if (filter.year && slip.year !== filter.year) return false;
    return true;
  });
});

const fetchPayslips = async () => {
  loading.value = true;
  try {
    const { data } = await api.get("/employee/payslips");
    payslips.value = data;
  } catch (err) {
    console.error(err);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchPayslips();
});
</script>