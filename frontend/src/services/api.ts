const API_BASE_URL = "http://127.0.0.1:8000/api";

export interface PingResponse {
  message: string;
  timestamp: string;
  status: string;
  vitals: {
    connected: boolean;
    ready: boolean;
    resolution: string;
    last_update: string;
  };
}

export const apiCall = async <T>(endpoint: string): Promise<T> => {
  try {
    const response = await fetch(`${API_BASE_URL}/${endpoint}`);
    if (!response.ok) {
      throw new Error(`API call failed with status ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
};

export const fetchPing = async (): Promise<PingResponse> => {
  return apiCall<PingResponse>("ping/");
};
