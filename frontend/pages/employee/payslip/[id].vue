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

        <!-- Loading -->
        <v-skeleton-loader v-if="loading" type="article" rounded="lg" />

        <template v-else-if="payslip">
          <!-- Header -->
          <div class="d-flex align-center mb-6">
            <v-btn icon variant="text" @click="router.back()" class="mr-2">
              <v-icon>mdi-arrow-left</v-icon>
            </v-btn>
            <h1 class="text-h5 font-weight-bold">
              สลิปเงินเดือน {{ monthName(payslip.month) }} {{ payslip.year + 543 }}
            </h1>
          </div>

          <!-- สลิป -->
          <v-card rounded="lg" elevation="2" id="payslip-card">
            <v-card-item class="bg-primary pa-6">
              <template #prepend>
                <v-avatar color="white" size="48">
                  <span class="text-primary font-weight-bold text-h6">A</span>
                </v-avatar>
              </template>
              <v-card-title class="text-white text-h6">บริษัท AKT Thailand</v-card-title>
              <v-card-subtitle class="text-white opacity-80">
                สลิปเงินเดือน · {{ monthName(payslip.month) }} {{ payslip.year + 543 }}
              </v-card-subtitle>
              <template #append>
                <div class="text-right">
                  <p class="text-white text-body-2 opacity-80">ลับเฉพาะ · STRICTLY CONFIDENTIAL</p>
                </div>
              </template>
            </v-card-item>

            <v-card-text class="pa-6">

              <!-- ข้อมูลพนักงาน -->
              <v-row class="mb-4">
                <v-col cols="12" sm="6">
                  <p class="text-body-2 text-medium-emphasis">ชื่อพนักงาน</p>
                  <p class="font-weight-medium">{{ payslip.employee.first_name }} {{ payslip.employee.last_name }}</p>
                </v-col>
                <v-col cols="12" sm="6">
                  <p class="text-body-2 text-medium-emphasis">รหัสพนักงาน</p>
                  <p class="font-weight-medium">{{ payslip.employee.employee_code }}</p>
                </v-col>
                <v-col cols="12" sm="6">
                  <p class="text-body-2 text-medium-emphasis">ตำแหน่ง</p>
                  <p class="font-weight-medium">{{ payslip.employee.position || '-' }}</p>
                </v-col>
                <v-col cols="12" sm="6">
                  <p class="text-body-2 text-medium-emphasis">แผนก</p>
                  <p class="font-weight-medium">{{ payslip.employee.department || '-' }}</p>
                </v-col>
              </v-row>

              <v-divider class="mb-4" />

              <!-- รายรับ / รายหัก -->
              <v-row>
                <!-- รายรับ -->
                <v-col cols="12" sm="6">
                  <p class="text-body-1 font-weight-bold mb-3">
                    <v-icon color="success" size="18" class="mr-1">mdi-plus-circle</v-icon>
                    รายการเงินได้
                  </p>
                  <div
                    v-for="item in earningItems"
                    :key="item.label"
                    class="d-flex justify-space-between mb-2"
                  >
                    <span class="text-body-2 text-medium-emphasis">{{ item.label }}</span>
                    <span class="text-body-2 font-weight-medium">
                      {{ item.value > 0 ? '฿' + formatNumber(item.value) : '—' }}
                    </span>
                  </div>
                  <v-divider class="my-2" />
                  <div class="d-flex justify-space-between">
                    <span class="font-weight-bold">รวมเงินได้</span>
                    <span class="font-weight-bold text-success">฿{{ formatNumber(payslip.total_income) }}</span>
                  </div>
                </v-col>

                <!-- รายหัก -->
                <v-col cols="12" sm="6">
                  <p class="text-body-1 font-weight-bold mb-3">
                    <v-icon color="error" size="18" class="mr-1">mdi-minus-circle</v-icon>
                    รายการเงินหัก
                  </p>
                  <div
                    v-for="item in deductionItems"
                    :key="item.label"
                    class="d-flex justify-space-between mb-2"
                  >
                    <span class="text-body-2 text-medium-emphasis">{{ item.label }}</span>
                    <span class="text-body-2 font-weight-medium">
                      {{ item.value > 0 ? '฿' + formatNumber(item.value) : '—' }}
                    </span>
                  </div>
                  <v-divider class="my-2" />
                  <div class="d-flex justify-space-between">
                    <span class="font-weight-bold">รวมเงินหัก</span>
                    <span class="font-weight-bold text-error">฿{{ formatNumber(payslip.total_deductions) }}</span>
                  </div>
                </v-col>
              </v-row>

              <v-divider class="my-4" />

              <!-- ยอดสุทธิ -->
              <v-sheet color="primary" rounded="lg" class="pa-4 d-flex justify-space-between align-center">
                <div>
                  <p class="text-white font-weight-bold text-body-1">เงินได้สุทธิ · NET PAY</p>
                  <p class="text-white opacity-80 text-body-2">โอนเข้าบัญชี</p>
                </div>
                <p class="text-white text-h5 font-weight-bold">฿{{ formatNumber(payslip.net_pay) }}</p>
              </v-sheet>

              <!-- สะสมประจำปี -->
              <div class="mt-4">
                <p class="text-body-2 font-weight-bold mb-3">สะสมตั้งแต่ต้นปี · YEAR-TO-DATE</p>
                <v-row>
                  <v-col cols="4" class="text-center">
                    <p class="text-body-2 text-medium-emphasis">รายได้สะสม</p>
                    <p class="font-weight-bold text-primary">฿{{ formatNumber(payslip.ytd_income) }}</p>
                  </v-col>
                  <v-col cols="4" class="text-center">
                    <p class="text-body-2 text-medium-emphasis">ภาษีสะสม</p>
                    <p class="font-weight-bold text-primary">฿{{ formatNumber(payslip.ytd_tax) }}</p>
                  </v-col>
                  <v-col cols="4" class="text-center">
                    <p class="text-body-2 text-medium-emphasis">ประกันสังคมสะสม</p>
                    <p class="font-weight-bold text-primary">฿{{ formatNumber(payslip.ytd_sso) }}</p>
                  </v-col>
                </v-row>
              </div>

            </v-card-text>
          </v-card>

        </template>

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
const route = useRoute()

const loading = ref(false)
const payslip = ref(null)

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

const earningItems = computed(() => [
  { label: 'เงินเดือน · Base Salary', value: payslip.value?.base_salary },
  { label: 'ค่าครองชีพ · COLA', value: payslip.value?.allowance },
  { label: 'โบนัส · Bonus', value: payslip.value?.special },
  { label: 'ค่าล่วงเวลา · Overtime', value: payslip.value?.overtime_hours },
  { label: 'เงินช่วยเหลือ · Allowance', value: payslip.value?.total_allowance },
  { label: 'รายการปรับ · Adjust', value: payslip.value?.adjust },
])

const deductionItems = computed(() => [
  { label: 'กองทุนสำรองเลี้ยงชีพ · PVD', value: payslip.value?.provident_fund },
  { label: 'ภาษีหัก ณ ที่จ่าย · WHT', value: payslip.value?.tax },
  { label: 'ประกันสังคม · SSO', value: payslip.value?.social_security },
  { label: 'รายการหัก · Deduct', value: payslip.value?.deduct },
])

const fetchPayslip = async () => {
  loading.value = true
  try {
    const { data } = await api.get(`/employee/payslips/${route.params.id}`)
    payslip.value = data
  } catch (err) {
    console.error(err)
    router.push('/employee/payslip')
  } finally {
    loading.value = false
  }
}

const logout = () => {
  auth.logout()
  router.push('/')
}

onMounted(() => {
  fetchPayslip()
})
</script>