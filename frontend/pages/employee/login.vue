<template>
  <v-app>
    <v-main class="bg-grey-lighten-3">
      <v-container class="fill-height" fluid>
        <v-row justify="center" align="center">
          <v-col cols="12" sm="6" md="4">
            <v-card rounded="lg" elevation="3" class="pa-6">

              <!-- Header -->
              <div class="text-center mb-6">
                <v-avatar color="secondary" size="56" class="mb-3">
                  <v-icon size="28" color="white">mdi-account</v-icon>
                </v-avatar>
                <h1 class="text-h6 font-weight-bold">เข้าสู่ระบบพนักงาน</h1>
                <p class="text-body-2 text-medium-emphasis mt-1">
                  ใช้เลขบัตรประชาชนและรหัสผ่าน
                </p>
              </div>

              <!-- Alert Error -->
              <v-alert
                v-if="errorMsg"
                type="error"
                variant="tonal"
                rounded="lg"
                class="mb-4"
                closable
                @click:close="errorMsg = ''"
              >
                {{ errorMsg }}
              </v-alert>

              <!-- Form -->
              <v-text-field
                v-model="form.national_id"
                label="เลขบัตรประชาชน 13 หลัก"
                prepend-inner-icon="mdi-card-account-details"
                variant="outlined"
                rounded="lg"
                class="mb-3"
                maxlength="13"
                :disabled="loading"
              />

              <v-text-field
                v-model="form.password"
                label="รหัสผ่าน"
                prepend-inner-icon="mdi-lock"
                :type="showPassword ? 'text' : 'password'"
                :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                @click:append-inner="showPassword = !showPassword"
                variant="outlined"
                rounded="lg"
                class="mb-4"
                :disabled="loading"
                @keyup.enter="login"
              />

              <v-alert
                type="info"
                variant="tonal"
                rounded="lg"
                class="mb-4"
                density="compact"
              >
                รหัสผ่านเริ่มต้นคือเลขบัตรประชาชนของท่าน
              </v-alert>

              <v-btn
                block
                color="secondary"
                size="large"
                rounded="lg"
                :loading="loading"
                @click="login"
              >
                เข้าสู่ระบบ
              </v-btn>

              <v-btn
                block
                variant="text"
                class="mt-2"
                to="/"
              >
                ย้อนกลับ
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
  middleware: 'guest'
})

const { api } = useApi()
const auth = useAuthStore()
const router = useRouter()

const form = reactive({
  national_id: '1101200132001',
  password: '1101200132001'
})

const loading = ref(false)
const errorMsg = ref('')
const showPassword = ref(false)

const login = async () => {
  if (!form.national_id || !form.password) {
    errorMsg.value = 'กรุณากรอกเลขบัตรประชาชนและรหัสผ่าน'
    return
  }

  if (form.national_id.length !== 13) {
    errorMsg.value = 'เลขบัตรประชาชนต้องมี 13 หลัก'
    return
  }

  loading.value = true
  errorMsg.value = ''

  try {
    const { data } = await api.post('/employee/login', {
      national_id: form.national_id,
      password: form.password
    })
    auth.setAuth(data.access_token, data.role)
    router.push('/employee/payslip')
  } catch (err) {
    errorMsg.value = err.response?.data?.detail || 'เกิดข้อผิดพลาด กรุณาลองใหม่'
  } finally {
    loading.value = false
  }
}
</script>