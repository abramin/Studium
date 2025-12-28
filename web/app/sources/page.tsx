import Link from 'next/link';
import { apiFetch } from '../../lib/api';
import type { Source } from '../../types/sources';

async function loadSources(): Promise<Source[]> {
  return apiFetch<Source[]>('/v1/sources');
}

function formatSize(bytes: number) {
  const kb = bytes / 1024;
  return `${kb.toFixed(1)} KB`;
}

export default async function SourcesPage() {
  const sources = await loadSources();

  return (
    <div>
      <h1>Sources</h1>
      {sources.length === 0 ? (
        <div className="card empty-state">No sources uploaded yet.</div>
      ) : (
        sources.map((source) => (
          <div key={source.id} className="card">
            <h3>
              <Link href={`/sources/${source.id}`}>{source.title}</Link>
            </h3>
            <p className="meta">
              {source.original_file_name} · {formatSize(source.file_size)} ·{' '}
              {new Date(source.created_at).toLocaleString()}
            </p>
            {source.description ? <p>{source.description}</p> : null}
          </div>
        ))
      )}
    </div>
  );
}
