<template>
  <v-app>
    <v-navigation-drawer permanent>
      <v-list-item
        prepend-icon="mdi-shield-account"
        title="Admin / HR"
        subtitle="ระบบสลิปเงินเดือน"
        class="py-4"
      />
      <v-divider />
      <v-list nav>
        <v-list-item
          prepend-icon="mdi-upload"
          title="อัพโหลดข้อมูล"
          to="/admin/upload"
          rounded="lg"
        />
        <v-list-item
          prepend-icon="mdi-history"
          title="ประวัติการอัพโหลด"
          to="/admin/history"
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
        <h1 class="text-h5 font-weight-bold mb-6">อัพโหลดข้อมูลเงินเดือน</h1>

        <v-row>
          <v-col cols="12" md="6">
            <v-card rounded="lg" elevation="2" class="pa-6">
              <v-row class="mb-4">
                <v-col cols="6">
                  <v-select
                    v-model="form.month"
                    :items="months"
                    item-title="label"
                    item-value="value"
                    label="เดือน"
                    variant="outlined"
                    rounded="lg"
                  />
                </v-col>
                <v-col cols="6">
                  <v-select
                    v-model="form.year"
                    :items="years"
                    label="ปี"
                    variant="outlined"
                    rounded="lg"
                  />
                </v-col>
              </v-row>

              <!-- Upload -->
              <v-sheet
                border
                rounded="lg"
                class="pa-8 text-center mb-4"
                :class="dragOver ? 'bg-primary-lighten-5' : 'bg-grey-lighten-4'"
                @dragover.prevent="dragOver = true"
                @dragleave="dragOver = false"
                @drop.prevent="onDrop"
              >
                <v-icon size="48" color="primary" class="mb-3">mdi-file-excel</v-icon>
                <p class="text-body-1 font-weight-medium">ลากไฟล์ Excel มาวางที่นี่</p>
                <p class="text-body-2 text-medium-emphasis mb-4">หรือ</p>
                <v-btn
                  variant="outlined"
                  color="primary"
                  rounded="lg"
                  @click="fileInput.click()"
                >
                  เลือกไฟล์
                </v-btn>
                <input
                  ref="fileInput"
                  type="file"
                  accept=".xlsx,.xls"
                  class="d-none"
                  @change="onFileChange"
                />
                <p v-if="file" class="mt-3 text-body-2 text-primary font-weight-medium">
                  <v-icon size="16">mdi-check-circle</v-icon>
                  {{ file.name }}
                </p>
              </v-sheet>

              <v-btn
                block
                color="primary"
                size="large"
                rounded="lg"
                :loading="loading"
                :disabled="!file || !form.month || !form.year"
                @click="upload"
              >
                <v-icon start>mdi-upload</v-icon>
                อัพโหลด
              </v-btn>

            </v-card>
          </v-col>

          <!-- result -->
          <v-col v-if="result" cols="12" md="6">
            <v-card rounded="lg" elevation="2" class="pa-6">
              <h2 class="text-h6 font-weight-bold mb-4">ผลการอัพโหลด</h2>

              <v-row class="mb-4">
                <v-col cols="4" class="text-center">
                  <p class="text-h4 font-weight-bold">{{ result.total_records }}</p>
                  <p class="text-body-2 text-medium-emphasis">ทั้งหมด</p>
                </v-col>
                <v-col cols="4" class="text-center">
                  <p class="text-h4 font-weight-bold text-success">{{ result.success_records }}</p>
                  <p class="text-body-2 text-medium-emphasis">สำเร็จ</p>
                </v-col>
                <v-col cols="4" class="text-center">
                  <p class="text-h4 font-weight-bold text-error">{{ result.failed_records }}</p>
                  <p class="text-body-2 text-medium-emphasis">ล้มเหลว</p>
                </v-col>
              </v-row>

              <v-alert
                v-if="result.errors.length === 0"
                type="success"
                variant="tonal"
                rounded="lg"
              >
                อัพโหลดสำเร็จทั้งหมด
              </v-alert>

              <div v-else>
                <p class="text-body-2 font-weight-medium mb-2">รายการที่มีปัญหา:</p>
                <v-alert
                  v-for="(err, i) in result.errors"
                  :key="i"
                  type="warning"
                  variant="tonal"
                  rounded="lg"
                  density="compact"
                  class="mb-2"
                >
                  {{ err }}
                </v-alert>
              </div>

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

const fileInput = ref(null)
const file = ref(null)
const loading = ref(false)
const dragOver = ref(false)
const result = ref(null)

const currentYear = new Date().getFullYear()

const months = [
  { label: 'มกราคม', value: 1 },
  { label: 'กุมภาพันธ์', value: 2 },
  { label: 'มีนาคม', value: 3 },
  { label: 'เมษายน', value: 4 },
  { label: 'พฤษภาคม', value: 5 },
  { label: 'มิถุนายน', value: 6 },
  { label: 'กรกฎาคม', value: 7 },
  { label: 'สิงหาคม', value: 8 },
  { label: 'กันยายน', value: 9 },
  { label: 'ตุลาคม', value: 10 },
  { label: 'พฤศจิกายน', value: 11 },
  { label: 'ธันวาคม', value: 12 },
]

const years = Array.from({ length: 5 }, (_, i) => currentYear - i)

const form = reactive({
  month: new Date().getMonth() + 1,
  year: currentYear
})

const onFileChange = (e) => {
  file.value = e.target.files[0]
}

const onDrop = (e) => {
  dragOver.value = false
  file.value = e.dataTransfer.files[0]
}

const upload = async () => {
  if (!file.value) return

  loading.value = true
  result.value = null

  try {
    const formData = new FormData()
    formData.append('file', file.value)

    const { data } = await api.post(
      `/admin/upload?month=${form.month}&year=${form.year}`,
      formData,
      { headers: { 'Content-Type': 'multipart/form-data' } }
    )
    result.value = data
  } catch (err) {
    result.value = {
      total_records: 0,
      success_records: 0,
      failed_records: 0,
      errors: [err.response?.data?.detail || 'เกิดข้อผิดพลาด']
    }
  } finally {
    loading.value = false
  }
}

const logout = () => {
  auth.logout()
  router.push('/')
}
</script>