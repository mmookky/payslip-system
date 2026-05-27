export default defineNuxtRouteMiddleware((to) => {
  const auth = useAuthStore()

  if (!auth.isLoggedIn) {
    return navigateTo('/')
  }

  if (to.path.startsWith('/employee') && !auth.isEmployee) {
    return navigateTo('/admin/upload')
  }

  if (to.path.startsWith('/admin') && !auth.isAdmin) {
    return navigateTo('/employee/payslip')
  }
})