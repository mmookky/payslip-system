export default defineNuxtRouteMiddleware(() => {
  const auth = useAuthStore()

  if (auth.isLoggedIn) {
    if (auth.isAdmin) {
      return navigateTo('/admin/upload')
    }
    return navigateTo('/employee/payslip')
  }
})