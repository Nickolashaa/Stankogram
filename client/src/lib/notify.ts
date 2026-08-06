import { toast } from "vue-sonner"

export const notify = {
  message: (text: string) => toast(text),
  success: (text: string) => toast.success(text),
  error: (text: string) => toast.error(text),
  info: (text: string) => toast.info(text),
  warning: (text: string) => toast.warning(text),
}
