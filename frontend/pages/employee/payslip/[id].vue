<template>
  <v-app class="bg-sky">
    <DrawerEmployee />
    <v-main>
      <v-container class="pa-6">
        <v-skeleton-loader v-if="loading" type="article" rounded="lg" />

        <template v-else-if="payslip">
          <!-- Actions -->
          <div class="d-flex align-center justify-space-between mb-6">
            <div class="d-flex align-center">
              <v-btn icon variant="text" @click="router.back()" class="mr-2">
                <v-icon>mdi-arrow-left</v-icon>
              </v-btn>
              <h1 class="text-h5 font-weight-bold">
                {{ monthName(payslip.month) }} {{ payslip.year }} Payslip
              </h1>
            </div>
            <v-btn
              color="secondary"
              variant="outlined"
              rounded="lg"
              :loading="downloading"
              @click="downloadPDF"
            >
              <v-icon start>mdi-file-pdf-box</v-icon>
              Download PDF
            </v-btn>
          </div>

          <v-card rounded="lg" elevation="2" id="payslip-card">
            <!-- Header -->
            <v-card-item class="bg-secondary pa-6">
              <template #prepend>
                <v-avatar color="white" size="48">
                  <span class="text-secondary font-weight-bold text-h6">A</span>
                </v-avatar>
              </template>
              <v-card-title class="text-white text-h6"
                >AKT Thailand Co., Ltd.</v-card-title
              >
              <v-card-subtitle class="text-white opacity-80">
                Payslip · {{ monthName(payslip.month) }} {{ payslip.year }}
              </v-card-subtitle>
              <template #append>
                <div class="text-right">
                  <p class="text-white text-body-2 font-weight-bold">
                    STRICTLY CONFIDENTIAL
                  </p>
                  <p class="text-white text-body-2 opacity-80">
                    Pay Date: 25 {{ monthName(payslip.month) }}
                    {{ payslip.year }}
                  </p>
                </div>
              </template>
            </v-card-item>

            <v-card-text class="pa-6">
              <!-- Employee Info -->
              <v-row class="mb-4">
                <v-col cols="12" sm="6">
                  <p class="text-body-2 text-medium-emphasis">Employee Name</p>
                  <p class="font-weight-medium">
                    {{ payslip.employee.first_name }}
                    {{ payslip.employee.last_name }}
                  </p>
                </v-col>
                <v-col cols="12" sm="6">
                  <p class="text-body-2 text-medium-emphasis">Employee Code</p>
                  <p class="font-weight-medium">
                    {{ payslip.employee.employee_code }}
                  </p>
                </v-col>
                <v-col cols="12" sm="6">
                  <p class="text-body-2 text-medium-emphasis">Position</p>
                  <p class="font-weight-medium">
                    {{ payslip.employee.position || "-" }}
                  </p>
                </v-col>
                <v-col cols="12" sm="6">
                  <p class="text-body-2 text-medium-emphasis">Department</p>
                  <p class="font-weight-medium">
                    {{ payslip.employee.department || "-" }}
                  </p>
                </v-col>
              </v-row>

              <v-divider class="mb-4" />

              <!-- Earnings / Deductions -->
              <v-row>
                <v-col cols="12" sm="6">
                  <p class="text-body-1 font-weight-bold mb-3">
                    <v-icon color="success" size="18" class="mr-1"
                      >mdi-plus-circle</v-icon
                    >
                    Earnings
                  </p>
                  <div
                    v-for="item in earningItems"
                    :key="item.label"
                    class="d-flex justify-space-between mb-2"
                  >
                    <span class="text-body-2 text-medium-emphasis">{{
                      item.label
                    }}</span>
                    <span class="text-body-2 font-weight-medium">
                      {{
                        item.value > 0 ? "฿" + formatNumber(item.value) : "—"
                      }}
                    </span>
                  </div>
                  <v-divider class="my-2" />
                  <div class="d-flex justify-space-between">
                    <span class="font-weight-bold">Total Earnings</span>
                    <span class="font-weight-bold text-success"
                      >฿{{ formatNumber(payslip.total_income) }}</span
                    >
                  </div>
                </v-col>

                <v-col cols="12" sm="6">
                  <p class="text-body-1 font-weight-bold mb-3">
                    <v-icon color="error" size="18" class="mr-1"
                      >mdi-minus-circle</v-icon
                    >
                    Deductions
                  </p>
                  <div
                    v-for="item in deductionItems"
                    :key="item.label"
                    class="d-flex justify-space-between mb-2"
                  >
                    <span class="text-body-2 text-medium-emphasis">{{
                      item.label
                    }}</span>
                    <span class="text-body-2 font-weight-medium">
                      {{
                        item.value > 0 ? "฿" + formatNumber(item.value) : "—"
                      }}
                    </span>
                  </div>
                  <v-divider class="my-2" />
                  <div class="d-flex justify-space-between">
                    <span class="font-weight-bold">Total Deductions</span>
                    <span class="font-weight-bold text-error"
                      >฿{{ formatNumber(payslip.total_deductions) }}</span
                    >
                  </div>
                </v-col>
              </v-row>

              <v-divider class="my-4" />

              <!-- Net Pay -->
              <v-sheet
                color="secondary"
                rounded="lg"
                class="pa-4 d-flex justify-space-between align-center"
              >
                <div>
                  <p class="text-white font-weight-bold text-body-1">NET PAY</p>
                  <p class="text-white opacity-80 text-body-2">
                    Transferred to Bank Account
                  </p>
                </div>
                <p class="text-white text-h5 font-weight-bold">
                  ฿{{ formatNumber(payslip.net_pay) }}
                </p>
              </v-sheet>

              <!-- YTD -->
              <div class="mt-4">
                <p class="text-body-2 font-weight-bold mb-3">
                  YEAR-TO-DATE SUMMARY
                </p>
                <v-row>
                  <v-col cols="4" class="text-center">
                    <p class="text-body-2 text-medium-emphasis">YTD Earnings</p>
                    <p class="font-weight-bold text-secondary">
                      ฿{{ formatNumber(payslip.ytd_income) }}
                    </p>
                  </v-col>
                  <v-col cols="4" class="text-center">
                    <p class="text-body-2 text-medium-emphasis">YTD Tax</p>
                    <p class="font-weight-bold text-secondary">
                      ฿{{ formatNumber(payslip.ytd_tax) }}
                    </p>
                  </v-col>
                  <v-col cols="4" class="text-center">
                    <p class="text-body-2 text-medium-emphasis">YTD SSO</p>
                    <p class="font-weight-bold text-secondary">
                      ฿{{ formatNumber(payslip.ytd_sso) }}
                    </p>
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
definePageMeta({ middleware: "auth" });

const { api } = useApi();
const router = useRouter();
const route = useRoute();

const loading = ref(false);
const downloading = ref(false);
const payslip = ref(null);

const formatNumber = (n) =>
  Number(n).toLocaleString("en-US", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });

const earningItems = computed(() => [
  { label: "Base Salary", value: payslip.value?.base_salary },
  { label: "COLA / Allowance", value: payslip.value?.allowance },
  { label: "Bonus / Special", value: payslip.value?.special },
  { label: "Overtime", value: payslip.value?.overtime_hours },
  { label: "Total Allowance", value: payslip.value?.total_allowance },
  { label: "Adjust", value: payslip.value?.adjust },
]);

const deductionItems = computed(() => [
  { label: "Provident Fund (PVD)", value: payslip.value?.provident_fund },
  { label: "Withholding Tax (WHT)", value: payslip.value?.tax },
  { label: "Social Security (SSO)", value: payslip.value?.social_security },
  { label: "Tax Allowance", value: payslip.value?.tax_allowance },
  { label: "Welfare Fund", value: payslip.value?.welfare_fund },
  { label: "Other Deductions", value: payslip.value?.deduct },
]);

const fetchPayslip = async () => {
  loading.value = true;
  try {
    const { data } = await api.get(`/employee/payslips/${route.params.id}`);
    payslip.value = data;
  } catch (err) {
    console.error(err);
    router.push("/employee/payslip");
  } finally {
    loading.value = false;
  }
};

const downloadPDF = async () => {
  downloading.value = true;
  try {
    const { default: html2canvas } = await import("html2canvas");
    const { default: jsPDF } = await import("jspdf");

    const element = document.getElementById("payslip-card");
    const canvas = await html2canvas(element, { scale: 2, useCORS: true });
    const imgData = canvas.toDataURL("image/png");

    const pdf = new jsPDF({
      orientation: "portrait",
      unit: "mm",
      format: "a4",
    });
    const pageWidth = pdf.internal.pageSize.getWidth();
    const pageHeight = pdf.internal.pageSize.getHeight();
    const imgWidth = pageWidth - 20;
    const imgHeight = (canvas.height * imgWidth) / canvas.width;

    pdf.addImage(
      imgData,
      "PNG",
      10,
      10,
      imgWidth,
      Math.min(imgHeight, pageHeight - 20)
    );
    pdf.save(
      `payslip_${monthName(payslip.value.month)}_${payslip.value.year}.pdf`
    );
  } catch (err) {
    console.error("PDF generation failed:", err);
  } finally {
    downloading.value = false;
  }
};

onMounted(() => {
  fetchPayslip();
});
</script>