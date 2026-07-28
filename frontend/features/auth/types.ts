export interface User {
  id: number;
  full_name: string;
  email: string;
  created_at: string;
  is_active: boolean;
  last_name_change: string | null;
  google_id: string | null;
}

export interface LoginPayload {
  email: string;
  password: string;
}

export interface RegisterPayload {
  full_name: string;
  email: string;
  password: string;
}