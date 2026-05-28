export default defineNuxtRouteMiddleware(() => {
  const token = useCookie('token')
  const role = useCookie('role')

  if (token.value) {
    if (role.value === 'admin') {
      return navigateTo('/admin/upload')
    }
    return navigateTo('/employee/payslip')
  }
})