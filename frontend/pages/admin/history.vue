<template>
  <v-app class="bg-honey">
    <DrawerAdmin />
    <v-main>
      <v-container class="pa-6">
        <h1 class="text-h5 font-weight-bold mb-6">Upload History</h1>
        <v-card rounded="lg" elevation="2">
          <v-data-table
            :headers="headers"
            :items="uploads"
            :loading="loading"
            rounded="lg"
          >
            <template #item.period="{ item }">
              {{ monthName(item.month) }} {{ item.year }}
            </template>

            <template #item.status="{ item }">
              <v-chip
                :color="item.status === 'completed' ? 'success' : 'error'"
                variant="tonal"
                size="small"
              >
                {{ item.status === "completed" ? "Success" : "Failed" }}
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

            <template #item.actions="{ item }">
              <v-btn
                icon
                size="small"
                variant="text"
                color="primary"
                @click="downloadOriginal(item.id, item.filename)"
              >
                <v-icon>mdi-download</v-icon>
                <v-tooltip activator="parent">Download Original</v-tooltip>
              </v-btn>
              <v-btn
                v-if="item.status === 'failed'"
                icon
                size="small"
                variant="text"
                color="error"
                @click="downloadError(item.id)"
              >
                <v-icon>mdi-alert-circle-outline</v-icon>
                <v-tooltip activator="parent">Download Error File</v-tooltip>
              </v-btn>
            </template>
          </v-data-table>
        </v-card>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
definePageMeta({ middleware: "auth" });

const { api } = useApi();
const loading = ref(false);
const uploads = ref([]);

const headers = [
  { title: "Filename", key: "filename" },
  { title: "Period", key: "period" },
  { title: "Success / Total", key: "records" },
  { title: "Status", key: "status" },
  { title: "Uploaded At", key: "uploaded_at" },
  { title: "Actions", key: "actions", sortable: false },
];

const formatDate = (dateStr) => {
  const d = new Date(dateStr);
  return d.toLocaleDateString("en-GB", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
};

const downloadFile = async (url, filename) => {
  try {
    const response = await api.get(url, { responseType: "blob" });
    const link = document.createElement("a");
    link.href = window.URL.createObjectURL(new Blob([response.data]));
    link.setAttribute("download", filename);
    document.body.appendChild(link);
    link.click();
    link.remove();
  } catch (err) {
    console.error("Download failed:", err);
  }
};

const downloadOriginal = (id, filename) =>
  downloadFile(`/admin/uploads/${id}/download-original`, filename);
const downloadError = (id) =>
  downloadFile(`/admin/uploads/${id}/download-error`, `error_${id}.xlsx`);

const fetchUploads = async () => {
  loading.value = true;
  try {
    const { data } = await api.get("/admin/uploads");
    uploads.value = data;
  } catch (err) {
    console.error(err);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchUploads();
});
</script>