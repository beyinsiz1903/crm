import { useRef, useState } from "react";
import { Upload, X, Image as ImageIcon } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { uploadFile } from "@/lib/api";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

export default function ImageUpload({ value, onChange, label, testId }) {
  const fileRef = useRef(null);
  const [uploading, setUploading] = useState(false);

  const handleUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setUploading(true);
    try {
      const result = await uploadFile(file);
      onChange(BACKEND_URL + result.url);
    } catch (err) {
      console.error("Upload failed:", err);
      alert("Yukleme basarisiz: " + (err.response?.data?.detail || err.message));
    } finally {
      setUploading(false);
      if (fileRef.current) fileRef.current.value = "";
    }
  };

  return (
    <div>
      {label && <label className="text-xs text-muted-foreground mb-1 block">{label}</label>}
      <div className="flex gap-2">
        <Input
          value={value || ""}
          onChange={(e) => onChange(e.target.value)}
          placeholder="Gorsel URL veya yukle"
          className="h-8 text-sm flex-1"
          data-testid={testId}
        />
        <Button
          type="button"
          variant="outline"
          size="icon"
          className="h-8 w-8 flex-shrink-0"
          onClick={() => fileRef.current?.click()}
          disabled={uploading}
          title="Gorsel Yukle"
        >
          {uploading ? (
            <span className="animate-spin text-xs">...</span>
          ) : (
            <Upload size={12} />
          )}
        </Button>
      </div>
      <input
        ref={fileRef}
        type="file"
        accept="image/*"
        onChange={handleUpload}
        className="hidden"
      />
      {value && (
        <div className="mt-2 relative rounded-md overflow-hidden h-16 bg-muted">
          <img src={value} alt="" className="w-full h-full object-cover" />
          <button
            onClick={() => onChange("")}
            className="absolute top-1 right-1 bg-background/80 rounded-full p-0.5 hover:bg-destructive/80"
          >
            <X size={10} />
          </button>
        </div>
      )}
    </div>
  );
}
