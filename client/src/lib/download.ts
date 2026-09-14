const XLSX_MEDIA_TYPE = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

export function downloadXlsx(filename: string, content: string) {
  const bytes = Uint8Array.from(atob(content), (character) => character.charCodeAt(0))
  const url = URL.createObjectURL(new Blob([bytes], { type: XLSX_MEDIA_TYPE }))

  const link = document.createElement("a")
  link.href = url
  link.download = filename
  link.click()

  URL.revokeObjectURL(url)
}
