import Link from 'next/link';
import { apiFetch } from '../../../lib/api';
import type { Source } from '../../../types/sources';

type SourcePageProps = {
  params: { id: string };
};

async function loadSource(id: string): Promise<Source> {
  return apiFetch<Source>(`/v1/sources/${id}`);
}

export default async function SourceDetailPage({ params }: SourcePageProps) {
  const { id } = params;
  const source = await loadSource(id);

  return (
    <div className="card">
      <div className="meta">
        <Link href="/sources">← Back to sources</Link>
      </div>
      <h1>{source.title}</h1>
      {source.description ? <p>{source.description}</p> : null}

      <div className="meta">
        <div>Original file: {source.original_file_name}</div>
        <div>MIME type: {source.content_type}</div>
        <div>Stored at: {source.file_path}</div>
        <div>Uploaded: {new Date(source.created_at).toLocaleString()}</div>
        <div>Owner: {source.owner_user_id ?? 'Unassigned'}</div>
      </div>
    </div>
  );
}
