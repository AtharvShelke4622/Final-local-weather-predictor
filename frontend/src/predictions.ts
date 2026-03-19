const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8002';

export interface PredictionTextResponse {
  device_id: string
  model_version: string
  generated_at: string
  prediction_text: Record<string, string[]>
}

export async function fetchPredictionText(deviceId: string): Promise<PredictionTextResponse> {
  const res = await fetch(
    `${API_BASE_URL}/api/v1/prediction-text?device_id=${deviceId}`,
    { mode: 'cors' }
  )

  if (!res.ok) {
    throw new Error(`Prediction text fetch failed (${res.status})`)
  }

  const data = await res.json()

  // 🛡️ HARD GUARANTEE SHAPE
  if (!data || typeof data !== 'object') {
    throw new Error('Invalid prediction text response')
  }

  data.prediction_text = data.prediction_text ?? {}

  return data
}
