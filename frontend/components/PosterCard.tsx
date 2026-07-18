import { Download, ImageOff } from "lucide-react";

export default function PosterCard({ posterUrl }: { posterUrl: string | null }) {
  return (
    <div className="stamp-border rounded-sm bg-surface p-6">
      <p className="font-mono text-xs tracking-widest text-muted uppercase mb-4">
        Exhibit B — career roadmap
      </p>
      {posterUrl ? (
        <div className="space-y-3">
          <img src={posterUrl} alt="Career roadmap poster" className="w-full rounded-sm" />
          <a
            href={posterUrl}
            download="career-roadmap.png"
            className="inline-flex items-center gap-2 font-mono text-xs uppercase tracking-widest text-teal hover:text-amber transition-colors"
          >
            <Download className="w-4 h-4" /> Download poster
          </a>
        </div>
      ) : (
        <div className="flex flex-col items-center justify-center gap-2 py-12 text-muted">
          <ImageOff className="w-6 h-6" />
          <p className="text-sm">Poster unavailable — image generation was skipped or failed.</p>
        </div>
      )}
    </div>
  );
}
