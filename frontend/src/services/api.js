import axios from "axios";

const baseUrl = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export async function uploadSalesFile({ file, email }) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("email", email);

  const url = `${baseUrl.replace(/\/+$/, "")}/api/upload`;

  const response = await axios.post(url, formData, {
    headers: {
      "Content-Type": "multipart/form-data"
    },
    timeout: 60000
  });

  return response.data;
}

