export default defineNuxtRouteMiddleware((to) => {
  const token = useCookie('token')
  const role = useCookie('role')

  if (!token.value) {
    return navigateTo('/')
  }

  if (to.path.startsWith('/employee') && role.value !== 'employee') {
    return navigateTo('/admin/upload')
  }

  if (to.path.startsWith('/admin') && role.value !== 'admin') {
    return navigateTo('/employee/payslip')
  }
})