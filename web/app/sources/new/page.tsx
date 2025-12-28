'use client';

import { useRouter } from 'next/navigation';
import { FormEvent, useState } from 'react';
import { apiBaseUrl } from '../../../lib/api';

export default function NewSourcePage() {
  const router = useRouter();
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setSubmitting(true);
    setError(null);

    const formData = new FormData(event.currentTarget);

    try {
      const response = await fetch(`${apiBaseUrl}/v1/sources`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const message = await response.text();
        throw new Error(message || 'Failed to upload source');
      }

      router.push('/sources');
      router.refresh();
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Upload failed';
      setError(message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="card">
      <h1>Add a Source</h1>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="title">Title</label>
          <input id="title" name="title" type="text" required placeholder="My PDF" />
        </div>

        <div className="form-group">
          <label htmlFor="description">Description</label>
          <textarea id="description" name="description" rows={4} placeholder="Optional context" />
        </div>

        <div className="form-group">
          <label htmlFor="file">PDF file</label>
          <input id="file" name="file" type="file" accept="application/pdf" required />
        </div>

        {error ? <div className="meta" style={{ color: 'crimson' }}>{error}</div> : null}

        <button className="button" type="submit" disabled={submitting}>
          {submitting ? 'Uploading…' : 'Upload PDF'}
        </button>
      </form>
    </div>
  );
}
