import { api } from './client';

export interface ImageCustomization {
  style: string;
  color_scheme: string;
  elements: string;
  mood: string;
  additional_details?: string;
}

export interface GenerateImageRequest {
  customization: ImageCustomization;
  ai_model?: string;
}

export interface ImageData {
  id: number;
  serial: string;
  image_url_verified: string;
  image_url_wallpaper: string;
  created_at: string;
  payment_status: string;
}

export interface VerifyResponse {
  valid: boolean;
  serial?: string;
  created_at?: string;
  image_url_verified?: string;
  user_email?: string;
}

export const imagesApi = {
  generate: async (data: GenerateImageRequest): Promise<ImageData> => {
    const response = await api.post<ImageData>('/api/generate-image', data);
    return response.data;
  },

  verify: async (serial: string): Promise<VerifyResponse> => {
    const response = await api.get<VerifyResponse>(`/api/verify/${serial}`);
    return response.data;
  },

  getMyImages: async (): Promise<ImageData[]> => {
    const response = await api.get<ImageData[]>('/api/my-images');
    return response.data;
  },
};
