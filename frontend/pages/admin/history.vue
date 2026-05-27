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
        <h1 class="text-h5 font-weight-bold mb-6">ประวัติการอัพโหลด</h1>

        <v-card rounded="lg" elevation="2">
          <v-data-table
            :headers="headers"
            :items="uploads"
            :loading="loading"
            rounded="lg"
          >
            <template #item.period="{ item }">
              {{ monthName(item.month) }} {{ item.year + 543 }}
            </template>

            <template #item.status="{ item }">
              <v-chip
                :color="item.failed_records > 0 ? 'warning' : 'success'"
                variant="tonal"
                size="small"
              >
                {{ item.failed_records > 0 ? 'มีข้อผิดพลาด' : 'สำเร็จ' }}
              </v-chip>
            </template>

            <template #item.records="{ item }">
              <span class="text-success">{{ item.success_records }}</span>
              /
              <span>{{ item.total_records }}</span>
            </template>

            <template #item.uploaded_at="{ item }">
              {{ formatDate(item.uploaded_at) }}
            </template>

          </v-data-table>
        </v-card>

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
const uploads = ref([])

const headers = [
  { title: 'ไฟล์', key: 'filename' },
  { title: 'งวดเงินเดือน', key: 'period' },
  { title: 'สำเร็จ / ทั้งหมด', key: 'records' },
  { title: 'สถานะ', key: 'status' },
  { title: 'วันที่อัพโหลด', key: 'uploaded_at' },
]

const monthNames = [
  'มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน',
  'พฤษภาคม', 'มิถุนายน', 'กรกฎาคม', 'สิงหาคม',
  'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม'
]

const monthName = (m) => monthNames[m - 1]

const formatDate = (dateStr) => {
  const d = new Date(dateStr)
  return d.toLocaleDateString('th-TH', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const fetchUploads = async () => {
  loading.value = true
  try {
    const { data } = await api.get('/admin/uploads')
    uploads.value = data
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
  fetchUploads()
})
</script>