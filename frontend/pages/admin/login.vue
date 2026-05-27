<template>
  <v-app>
    <v-main class="bg-grey-lighten-3">
      <v-container class="fill-height" fluid>
        <v-row justify="center" align="center">
          <v-col cols="12" sm="6" md="4">
            <v-card rounded="lg" elevation="3" class="pa-6">

              <div class="text-center mb-6">
                <v-avatar color="primary" size="56" class="mb-3">
                  <v-icon size="28" color="white">mdi-shield-account</v-icon>
                </v-avatar>
                <h1 class="text-h6 font-weight-bold">Admin / HR Login</h1>
              </div>

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
                v-model="form.username"
                label="ชื่อผู้ใช้"
                prepend-inner-icon="mdi-account"
                variant="outlined"
                rounded="lg"
                class="mb-3"
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

              <v-btn
                block
                color="primary"
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
  username: 'admin',
  password: 'admin1234'
})

const loading = ref(false)
const errorMsg = ref('')
const showPassword = ref(false)

const login = async () => {
  if (!form.username || !form.password) {
    errorMsg.value = 'กรุณากรอกชื่อผู้ใช้และรหัสผ่าน'
    return
  }

  loading.value = true
  errorMsg.value = ''

  try {
    const { data } = await api.post('/admin/login', {
      username: form.username,
      password: form.password
    })
    auth.setAuth(data.access_token, data.role)
    router.push('/admin/upload')
  } catch (err) {
    errorMsg.value = err.response?.data?.detail || 'เกิดข้อผิดพลาด กรุณาลองใหม่'
  } finally {
    loading.value = false
  }
}
</script>