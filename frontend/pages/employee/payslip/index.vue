<template>
  <v-app>
    <v-navigation-drawer permanent>
      <v-list-item
        prepend-icon="mdi-account"
        title="พนักงาน"
        subtitle="ระบบสลิปเงินเดือน"
        class="py-4"
      />
      <v-divider />
      <v-list nav>
        <v-list-item
          prepend-icon="mdi-file-document-multiple"
          title="สลิปเงินเดือน"
          to="/employee/payslip"
          rounded="lg"
        />
      </v-list>
      <template #append>
        <div class="pa-3">
          <v-btn block variant="tonal" color="error" @click="logout">
            <v-icon start>mdi-logout</v-icon>
            ออกจากระบบ
          </v-btn>
        </div>
      </template>
    </v-navigation-drawer>

    <v-main>
      <v-container class="pa-6">
        <h1 class="text-h5 font-weight-bold mb-6">สลิปเงินเดือนของฉัน</h1>

        <!-- Loading -->
        <v-row v-if="loading">
          <v-col v-for="i in 3" :key="i" cols="12" sm="6" md="4">
            <v-skeleton-loader type="card" rounded="lg" />
          </v-col>
        </v-row>

        <!-- ไม่มีข้อมูล -->
        <v-card v-else-if="payslips.length === 0" rounded="lg" elevation="2" class="pa-8 text-center">
          <v-icon size="64" color="grey-lighten-1" class="mb-4">mdi-file-document-off</v-icon>
          <p class="text-h6 text-medium-emphasis">ยังไม่มีข้อมูลสลิปเงินเดือน</p>
        </v-card>

        <!-- รายการสลิป -->
        <v-row v-else>
          <v-col
            v-for="slip in payslips"
            :key="slip.id"
            cols="12" sm="6" md="4"
          >
            <v-card
              rounded="lg"
              elevation="2"
              hover
              @click="router.push(`/employee/payslip/${slip.id}`)"
            >
              <v-card-item>
                <template #prepend>
                  <v-avatar color="primary" variant="tonal">
                    <v-icon>mdi-file-document</v-icon>
                  </v-avatar>
                </template>
                <v-card-title>{{ monthName(slip.month) }} {{ slip.year + 543 }}</v-card-title>
                <v-card-subtitle>สลิปเงินเดือน</v-card-subtitle>
              </v-card-item>

              <v-divider />

              <v-card-text>
                <div class="d-flex justify-space-between align-center">
                  <span class="text-body-2 text-medium-emphasis">ยอดสุทธิ</span>
                  <span class="text-h6 font-weight-bold text-primary">
                    ฿{{ formatNumber(slip.net_pay) }}
                  </span>
                </div>
              </v-card-text>

              <v-card-actions>
                <v-spacer />
                <v-btn
                  color="primary"
                  variant="text"
                  :to="`/employee/payslip/${slip.id}`"
                >
                  ดูรายละเอียด
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
definePageMeta({
  middleware: 'auth'
})

const { api } = useApi()
const auth = useAuthStore()
const router = useRouter()

const loading = ref(false)
const payslips = ref([])

const monthNames = [
  'มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน',
  'พฤษภาคม', 'มิถุนายน', 'กรกฎาคม', 'สิงหาคม',
  'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม'
]

const monthName = (m) => monthNames[m - 1]

const formatNumber = (n) => {
  return Number(n).toLocaleString('th-TH', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })
}

const fetchPayslips = async () => {
  loading.value = true
  try {
    const { data } = await api.get('/employee/payslips')
    payslips.value = data
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

const logout = () => {
  auth.logout()
  router.push('/')
}

onMounted(() => {
  fetchPayslips()
})
</script>