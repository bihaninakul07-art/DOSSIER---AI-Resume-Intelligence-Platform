"use client";

import { useRef, useState } from "react";
import { motion } from "framer-motion";
import { FileText, UploadCloud } from "lucide-react";

export default function UploadZone({
  onFile,
  disabled,
}: {
  onFile: (file: File) => void;
  disabled?: boolean;
}) {
  const [dragging, setDragging] = useState(false);
  const [fileName, setFileName] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  function handleFile(file: File | undefined) {
    if (!file) return;
    if (file.type !== "application/pdf") return;
    setFileName(file.name);
    onFile(file);
  }

  return (
    <motion.div
      whileHover={{ scale: disabled ? 1 : 1.01 }}
      whileTap={{ scale: disabled ? 1 : 0.99 }}
      onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
      onDragLeave={() => setDragging(false)}
      onDrop={(e) => {
        e.preventDefault();
        setDragging(false);
        handleFile(e.dataTransfer.files?.[0]);
      }}
      onClick={() => !disabled && inputRef.current?.click()}
      className={`stamp-border rounded-sm p-12 text-center cursor-pointer transition-colors relative overflow-hidden
        ${dragging ? "bg-surface2 border-amber" : "bg-surface/70 backdrop-blur hover:bg-surface2"}
        ${disabled ? "opacity-50 pointer-events-none" : ""}`}
    >
      {dragging && (
        <motion.div
          className="absolute inset-0"
          style={{ background: "linear-gradient(90deg, #3FA79622, #8B7FE822, #E876B022)" }}
          animate={{ opacity: [0.4, 0.8, 0.4] }}
          transition={{ duration: 1.2, repeat: Infinity }}
        />
      )}
      <input
        ref={inputRef}
        type="file"
        accept="application/pdf"
        className="hidden"
        onChange={(e) => handleFile(e.target.files?.[0])}
      />
      <div className="flex flex-col items-center gap-3 relative">
        <motion.div
          animate={dragging ? { y: [0, -6, 0] } : {}}
          transition={{ duration: 0.8, repeat: Infinity }}
        >
          {fileName ? <FileText className="w-8 h-8 text-teal" /> : <UploadCloud className="w-8 h-8 text-muted" />}
        </motion.div>
        <p className="font-mono text-xs tracking-widest text-muted uppercase">
          {fileName ? "Exhibit A — attached" : "Submit exhibit for review"}
        </p>
        <p className="font-display text-xl text-text">
          {fileName || "Drop your resume PDF here"}
        </p>
        <p className="text-sm text-muted">or click to browse — PDF only</p>
      </div>
    </motion.div>
  );
}
