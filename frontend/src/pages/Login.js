import { useState } from "react";
import { motion } from "framer-motion";
import { Lock, Mail, User, ArrowRight } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { login, register } from "@/lib/api";

export default function Login({ mode: initialMode, onSuccess }) {
  const [mode, setMode] = useState(initialMode || "login");
  const [form, setForm] = useState({ email: "", password: "", name: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      let result;
      if (mode === "register") {
        if (!form.email || !form.password) {
          setError("E-posta ve sifre gerekli");
          setLoading(false);
          return;
        }
        result = await register(form);
      } else {
        result = await login({ email: form.email, password: form.password });
      }
      localStorage.setItem("syroce_token", result.token);
      onSuccess?.();
    } catch (err) {
      setError(err.response?.data?.detail || "Bir hata olustu");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-md"
      >
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="w-16 h-16 rounded-2xl bg-primary flex items-center justify-center mx-auto mb-4">
            <span className="text-primary-foreground font-bold text-3xl">S</span>
          </div>
          <h1 className="text-2xl font-bold">Syroce CRM</h1>
          <p className="text-sm text-muted-foreground mt-2">
            {mode === "register" ? "Hesabinizi olusturun" : "Hesabiniza giris yapin"}
          </p>
        </div>

        <Card className="border-border/50">
          <CardContent className="p-6">
            <form onSubmit={handleSubmit} className="space-y-4">
              {mode === "register" && (
                <div>
                  <label className="text-xs text-muted-foreground mb-1.5 block">Ad Soyad</label>
                  <div className="relative">
                    <User size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
                    <Input
                      value={form.name}
                      onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
                      placeholder="Admin"
                      className="pl-9"
                      data-testid="login-name-input"
                    />
                  </div>
                </div>
              )}
              <div>
                <label className="text-xs text-muted-foreground mb-1.5 block">E-posta</label>
                <div className="relative">
                  <Mail size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
                  <Input
                    type="email"
                    value={form.email}
                    onChange={(e) => setForm((f) => ({ ...f, email: e.target.value }))}
                    placeholder="admin@syroce.com"
                    className="pl-9"
                    data-testid="login-email-input"
                    required
                  />
                </div>
              </div>
              <div>
                <label className="text-xs text-muted-foreground mb-1.5 block">Sifre</label>
                <div className="relative">
                  <Lock size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
                  <Input
                    type="password"
                    value={form.password}
                    onChange={(e) => setForm((f) => ({ ...f, password: e.target.value }))}
                    placeholder="Sifreniz"
                    className="pl-9"
                    data-testid="login-password-input"
                    required
                  />
                </div>
              </div>
              {error && (
                <p className="text-xs text-destructive bg-destructive/10 rounded-lg px-3 py-2">{error}</p>
              )}
              <Button type="submit" className="w-full" disabled={loading} data-testid="login-submit">
                {loading ? "Yukleniyor..." : (mode === "register" ? "Hesap Olustur" : "Giris Yap")}
                <ArrowRight size={16} className="ml-2" />
              </Button>
            </form>
            {mode === "login" && (
              <p className="text-xs text-center text-muted-foreground mt-4">
                Hesabiniz yok mu?{" "}
                <button onClick={() => setMode("register")} className="text-primary hover:underline">
                  Kayit Ol
                </button>
              </p>
            )}
            {mode === "register" && (
              <p className="text-xs text-center text-muted-foreground mt-4">
                Zaten hesabiniz var mi?{" "}
                <button onClick={() => setMode("login")} className="text-primary hover:underline">
                  Giris Yap
                </button>
              </p>
            )}
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}
