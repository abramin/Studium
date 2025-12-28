export type Source = {
  id: string;
  title: string;
  description?: string | null;
  owner_user_id?: string | null;
  original_file_name: string;
  content_type: string;
  file_path: string;
  file_size: number;
  created_at: string;
  updated_at: string;
};
