<template>
  <v-app>
    <v-navigation-drawer permanent>
      <v-list-item
        prepend-icon="mdi-shield-account"
        title="Admin / HR"
        subtitle="Payslip System"
        class="py-4"
      />
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
          <v-btn block variant="tonal" color="error" @click="logout">
            <v-icon start>mdi-logout</v-icon>
            Logout
          </v-btn>
        </div>
      </template>
    </v-navigation-drawer>

    <v-main>
      <v-container class="pa-6">
        <h1 class="text-h5 font-weight-bold mb-6">Payslip Result</h1>

        <!-- Filter -->
        <v-card rounded="lg" elevation="2" class="pa-4 mb-4">
          <v-row align="center">
            <v-col cols="12" sm="4" md="3">
              <v-select
                v-model="filter.month"
                :items="months"
                item-title="label"
                item-value="value"
                label="Month"
                variant="outlined"
                rounded="lg"
                density="compact"
                hide-details
              />
            </v-col>
            <v-col cols="12" sm="4" md="3">
              <v-select
                v-model="filter.year"
                :items="years"
                label="Year"
                variant="outlined"
                rounded="lg"
                density="compact"
                hide-details
              />
            </v-col>
            <v-col cols="12" sm="4" md="2">
              <v-btn
                color="primary"
                rounded="lg"
                @click="fetchPayslips"
                :loading="loading"
              >
                <v-icon start>mdi-magnify</v-icon>
                Search
              </v-btn>
            </v-col>
          </v-row>
        </v-card>

        <!-- Table -->
        <v-card rounded="lg" elevation="2">
          <v-data-table
            :headers="headers"
            :items="payslips"
            :loading="loading"
            rounded="lg"
          >
            <template #item.name="{ item }">
              {{ item.employee.first_name }} {{ item.employee.last_name }}
            </template>

            <template #item.employee_code="{ item }">
              {{ item.employee.employee_code }}
            </template>

            <template #item.department="{ item }">
              {{ item.employee.department || '-' }}
            </template>

            <template #item.position="{ item }">
              {{ item.employee.position || '-' }}
            </template>

            <template #item.base_salary="{ item }">
              {{ formatNumber(item.base_salary) }}
            </template>

            <template #item.total_income="{ item }">
              {{ formatNumber(item.total_income) }}
            </template>

            <template #item.total_deductions="{ item }">
              {{ formatNumber(item.total_deductions) }}
            </template>

            <template #item.net_pay="{ item }">
              <span class="font-weight-bold text-primary">
                {{ formatNumber(item.net_pay) }}
              </span>
            </template>

            <template #no-data>
              <div class="text-center pa-6 text-medium-emphasis">
                No data found for {{ monthName(filter.month) }} {{ filter.year }}
              </div>
            </template>

          </v-data-table>
        </v-card>

      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
definePageMeta({ middleware: 'auth' })

const { api } = useApi()
const auth = useAuthStore()
const router = useRouter()

const loading = ref(false)
const payslips = ref([])

const currentYear = new Date().getFullYear()

const months = [
  { label: 'January', value: 1 },
  { label: 'February', value: 2 },
  { label: 'March', value: 3 },
  { label: 'April', value: 4 },
  { label: 'May', value: 5 },
  { label: 'June', value: 6 },
  { label: 'July', value: 7 },
  { label: 'August', value: 8 },
  { label: 'September', value: 9 },
  { label: 'October', value: 10 },
  { label: 'November', value: 11 },
  { label: 'December', value: 12 },
]

const years = Array.from({ length: 5 }, (_, i) => currentYear - i)

const monthNames = [
  'January', 'February', 'March', 'April',
  'May', 'June', 'July', 'August',
  'September', 'October', 'November', 'December'
]

const monthName = (m) => monthNames[m - 1]

const filter = reactive({
  month: new Date().getMonth() + 1,
  year: currentYear
})

const headers = [
  { title: 'Employee Code', key: 'employee_code' },
  { title: 'Name', key: 'name' },
  { title: 'Department', key: 'department' },
  { title: 'Position', key: 'position' },
  { title: 'Base Salary', key: 'base_salary' },
  { title: 'Total Income', key: 'total_income' },
  { title: 'Total Deductions', key: 'total_deductions' },
  { title: 'Net Pay', key: 'net_pay' },
]

const formatNumber = (n) => Number(n).toLocaleString('en-US', {
  minimumFractionDigits: 2,
  maximumFractionDigits: 2
})

const fetchPayslips = async () => {
  loading.value = true
  try {
    const { data } = await api.get(`/admin/payslips?month=${filter.month}&year=${filter.year}`)
    payslips.value = data
  } catch (err) {
    console.error(err)
    payslips.value = []
  } finally {
    loading.value = false
  }
}

const logout = () => { auth.logout(); router.push('/') }

onMounted(() => { fetchPayslips() })
</script>