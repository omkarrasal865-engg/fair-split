const API_BASE_URL = 
  process.env.NEXT_PUBLIC_API_URL ||
  "http://127.0.0.1:8000";

export async function splitBill(
  file: File,
  description: string
) {
  const formData = new FormData();

  formData.append("file", file);
  formData.append("description", description);

  const response = await fetch(
    `${API_BASE_URL}/split-bill-image`,
    {
      method: "POST",
      body: formData,
    }
  );

  if (!response.ok) {
    throw new Error("Failed to process receipt");
  }

  return response.json();
}