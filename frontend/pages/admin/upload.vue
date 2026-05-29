<template>
  <v-app class="bg-honey">
    <DrawerAdmin />
    <v-main>
      <v-container class="pa-6">
        <h1 class="text-h5 font-weight-bold mb-6">Upload Payslip Data</h1>
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
                    label="Month"
                    variant="outlined"
                    rounded="lg"
                  />
                </v-col>
                <v-col cols="6">
                  <v-select
                    v-model="form.year"
                    :items="years"
                    label="Year"
                    variant="outlined"
                    rounded="lg"
                  />
                </v-col>
              </v-row>

              <!-- Upload Zone -->
              <v-sheet
                border
                rounded="lg"
                class="pa-8 text-center mb-4"
                :class="dragOver ? 'bg-primary-lighten-5' : 'bg-grey-lighten-4'"
                @dragover.prevent="dragOver = true"
                @dragleave="dragOver = false"
                @drop.prevent="onDrop"
              >
                <v-icon size="48" color="primary" class="mb-3"
                  >mdi-file-excel</v-icon
                >
                <p class="text-body-1 font-weight-medium">
                  Drag & Drop Excel file here
                </p>
                <p class="text-body-2 text-medium-emphasis mb-4">or</p>
                <v-btn
                  variant="outlined"
                  color="primary"
                  rounded="lg"
                  @click="fileInput.click()"
                >
                  Browse File
                </v-btn>
                <input
                  ref="fileInput"
                  type="file"
                  accept=".xlsx,.xls"
                  class="d-none"
                  @change="onFileChange"
                />
                <p
                  v-if="file"
                  class="mt-3 text-body-2 text-primary font-weight-medium"
                >
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
                Upload
              </v-btn>
            </v-card>
          </v-col>

          <!-- ผลการ Upload -->
          <v-col v-if="result" cols="12" md="6">
            <v-card rounded="lg" elevation="2" class="pa-6">
              <div class="d-flex justify-space-between align-center mb-4">
                <h2 class="text-h6 font-weight-bold">Upload Result</h2>
                <v-chip
                  :color="result.status === 'completed' ? 'success' : 'error'"
                  variant="tonal"
                >
                  {{ result.status === "completed" ? "Success" : "Failed" }}
                </v-chip>
              </div>

              <!-- Summary -->
              <v-row class="mb-4">
                <v-col cols="4" class="text-center">
                  <p class="text-h4 font-weight-bold">
                    {{ result.total_records }}
                  </p>
                  <p class="text-body-2 text-medium-emphasis">Total</p>
                </v-col>
                <v-col cols="4" class="text-center">
                  <p class="text-h4 font-weight-bold text-success">
                    {{ result.success_records }}
                  </p>
                  <p class="text-body-2 text-medium-emphasis">Success</p>
                </v-col>
                <v-col cols="4" class="text-center">
                  <p class="text-h4 font-weight-bold text-error">
                    {{ result.failed_records }}
                  </p>
                  <p class="text-body-2 text-medium-emphasis">Failed</p>
                </v-col>
              </v-row>

              <!-- Success -->
              <v-alert
                v-if="
                  result.status === 'completed' && result.errors.length === 0
                "
                type="success"
                variant="tonal"
                rounded="lg"
                class="mb-3"
              >
                All records uploaded successfully.
              </v-alert>

              <!-- Global warnings -->
              <v-alert
                v-if="result.errors.length > 0 && result.status === 'completed'"
                type="warning"
                variant="tonal"
                rounded="lg"
                class="mb-3"
              >
                {{ result.errors[0] }}
              </v-alert>

              <!-- Error list -->
              <div v-if="result.status === 'failed'">
                <v-alert type="error" variant="tonal" rounded="lg" class="mb-3">
                  Upload failed. Please fix the errors below and re-upload.
                </v-alert>

                <!-- Download error file -->
                <v-btn
                  v-if="result.has_error_file"
                  block
                  color="error"
                  variant="outlined"
                  rounded="lg"
                  class="mb-3"
                  @click="downloadErrorFile(result.id)"
                >
                  <v-icon start>mdi-download</v-icon>
                  Download Error File
                </v-btn>

                <!-- Error details -->
                <v-expansion-panels variant="accordion">
                  <v-expansion-panel title="View Error Details">
                    <v-expansion-panel-text>
                      <v-list density="compact">
                        <v-list-item
                          v-for="(err, i) in result.errors"
                          :key="i"
                          prepend-icon="mdi-alert-circle"
                          base-color="error"
                        >
                          <v-list-item-subtitle class="text-wrap">
                            {{ err }}
                          </v-list-item-subtitle>
                        </v-list-item>
                      </v-list>
                    </v-expansion-panel-text>
                  </v-expansion-panel>
                </v-expansion-panels>
              </div>
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
const auth = useAuthStore();
const router = useRouter();

const fileInput = ref(null);
const file = ref(null);
const loading = ref(false);
const dragOver = ref(false);
const result = ref(null);

const currentYear = new Date().getFullYear();

const months = [
  { label: "January", value: 1 },
  { label: "February", value: 2 },
  { label: "March", value: 3 },
  { label: "April", value: 4 },
  { label: "May", value: 5 },
  { label: "June", value: 6 },
  { label: "July", value: 7 },
  { label: "August", value: 8 },
  { label: "September", value: 9 },
  { label: "October", value: 10 },
  { label: "November", value: 11 },
  { label: "December", value: 12 },
];

const years = Array.from({ length: 5 }, (_, i) => currentYear - i);

const form = reactive({
  month: new Date().getMonth() + 1,
  year: currentYear,
});

const onFileChange = (e) => {
  file.value = e.target.files[0];
};
const onDrop = (e) => {
  dragOver.value = false;
  file.value = e.dataTransfer.files[0];
};

const upload = async () => {
  if (!file.value) return;
  loading.value = true;
  result.value = null;
  try {
    const formData = new FormData();
    formData.append("file", file.value);
    const { data } = await api.post(
      `/admin/upload?month=${form.month}&year=${form.year}`,
      formData,
      { headers: { "Content-Type": "multipart/form-data" } }
    );
    result.value = data;
  } catch (err) {
    result.value = {
      total_records: 0,
      success_records: 0,
      failed_records: 0,
      status: "failed",
      has_error_file: false,
      errors: [
        err.response?.data?.detail || "An error occurred. Please try again.",
      ],
    };
  } finally {
    loading.value = false;
  }
};

const downloadErrorFile = async (uploadId) => {
  try {
    const response = await api.get(
      `/admin/uploads/${uploadId}/download-error`,
      {
        responseType: "blob",
      }
    );
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", `error_file.xlsx`);
    document.body.appendChild(link);
    link.click();
    link.remove();
  } catch (err) {
    console.error("Download failed:", err);
  }
};

const logout = () => {
  auth.logout();
  router.push("/");
};
</script>