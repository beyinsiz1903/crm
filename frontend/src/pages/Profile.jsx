import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { User, Mail, Lock, Save, Shield, Calendar, LogOut } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import PageHeader from "@/components/PageHeader";
import { getMe, updateProfile, changePassword } from "@/lib/api";

export default function Profile() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [profileForm, setProfileForm] = useState({ name: "", email: "" });
  const [passwordForm, setPasswordForm] = useState({ current_password: "", new_password: "", confirm_password: "" });
  const [profileSaving, setProfileSaving] = useState(false);
  const [passwordSaving, setPasswordSaving] = useState(false);
  const [profileMsg, setProfileMsg] = useState({ type: "", text: "" });
  const [passwordMsg, setPasswordMsg] = useState({ type: "", text: "" });

  useEffect(() => {
    getMe()
      .then((data) => {
        setUser(data);
        setProfileForm({ name: data.name || "", email: data.email || "" });
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const handleProfileSave = async (e) => {
    e.preventDefault();
    setProfileSaving(true);
    setProfileMsg({ type: "", text: "" });
    try {
      const updated = await updateProfile(profileForm);
      setUser((u) => ({ ...u, ...updated }));
      localStorage.setItem("syroce_user", JSON.stringify({ ...user, ...updated }));
      setProfileMsg({ type: "success", text: "Profil basariyla guncellendi!" });
    } catch (err) {
      setProfileMsg({ type: "error", text: err.response?.data?.detail || "Guncelleme hatasi" });
    } finally {
      setProfileSaving(false);
    }
  };

  const handlePasswordChange = async (e) => {
    e.preventDefault();
    setPasswordSaving(true);
    setPasswordMsg({ type: "", text: "" });
    if (passwordForm.new_password !== passwordForm.confirm_password) {
      setPasswordMsg({ type: "error", text: "Yeni sifreler eslesmiyor" });
      setPasswordSaving(false);
      return;
    }
    if (passwordForm.new_password.length < 6) {
      setPasswordMsg({ type: "error", text: "Yeni sifre en az 6 karakter olmali" });
      setPasswordSaving(false);
      return;
    }
    try {
      await changePassword({
        current_password: passwordForm.current_password,
        new_password: passwordForm.new_password,
      });
      setPasswordMsg({ type: "success", text: "Sifre basariyla degistirildi!" });
      setPasswordForm({ current_password: "", new_password: "", confirm_password: "" });
    } catch (err) {
      setPasswordMsg({ type: "error", text: err.response?.data?.detail || "Sifre degistirme hatasi" });
    } finally {
      setPasswordSaving(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("syroce_token");
    localStorage.removeItem("syroce_user");
    window.location.reload();
  };

  if (loading) {
    return (
      <div className="page-content">
        <div className="animate-pulse space-y-6">
          <div className="h-8 w-48 bg-muted rounded" />
          <div className="h-64 bg-muted rounded-xl" />
        </div>
      </div>
    );
  }

  const roleLabels = { admin: "Admin", editor: "Editor", viewer: "Goruntuleyici" };
  const roleColors = { admin: "bg-red-500/20 text-red-400", editor: "bg-blue-500/20 text-blue-400", viewer: "bg-gray-500/20 text-gray-400" };

  return (
    <div className="page-content">
      <PageHeader title="Profil Ayarlari" subtitle="Hesap bilgilerinizi yonetin" />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* User Info Card */}
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
          <Card>
            <CardContent className="p-6 text-center">
              <div className="w-20 h-20 rounded-full bg-primary/20 flex items-center justify-center mx-auto mb-4">
                <User size={36} className="text-primary" />
              </div>
              <h3 className="text-lg font-bold">{user?.name || "Kullanici"}</h3>
              <p className="text-sm text-muted-foreground mb-3">{user?.email}</p>
              <Badge className={`${roleColors[user?.role] || roleColors.viewer} text-xs`}>
                <Shield size={12} className="mr-1" />
                {roleLabels[user?.role] || user?.role}
              </Badge>
              <Separator className="my-4" />
              <div className="text-xs text-muted-foreground flex items-center justify-center gap-1">
                <Calendar size={12} />
                <span>Hesap ID: {user?.id?.slice(0, 8)}...</span>
              </div>
              <Button variant="outline" className="w-full mt-4 text-red-400 border-red-500/30 hover:bg-red-500/10" onClick={handleLogout}>
                <LogOut size={14} className="mr-2" /> Cikis Yap
              </Button>
            </CardContent>
          </Card>
        </motion.div>

        {/* Profile Edit */}
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="lg:col-span-2 space-y-6">
          <Card>
            <CardContent className="p-6">
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <User size={18} className="text-primary" /> Profil Bilgileri
              </h3>
              <form onSubmit={handleProfileSave} className="space-y-4">
                <div>
                  <label className="text-xs text-muted-foreground mb-1.5 block">Ad Soyad</label>
                  <div className="relative">
                    <User size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
                    <Input
                      value={profileForm.name}
                      onChange={(e) => setProfileForm((f) => ({ ...f, name: e.target.value }))}
                      className="pl-9"
                      placeholder="Adiniz"
                    />
                  </div>
                </div>
                <div>
                  <label className="text-xs text-muted-foreground mb-1.5 block">E-posta</label>
                  <div className="relative">
                    <Mail size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
                    <Input
                      value={profileForm.email}
                      onChange={(e) => setProfileForm((f) => ({ ...f, email: e.target.value }))}
                      className="pl-9"
                      type="email"
                      placeholder="E-posta adresiniz"
                    />
                  </div>
                </div>
                {profileMsg.text && (
                  <p className={`text-sm ${profileMsg.type === "success" ? "text-green-400" : "text-red-400"}`}>
                    {profileMsg.text}
                  </p>
                )}
                <Button type="submit" disabled={profileSaving} className="w-full">
                  <Save size={14} className="mr-2" /> {profileSaving ? "Kaydediliyor..." : "Kaydet"}
                </Button>
              </form>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Lock size={18} className="text-primary" /> Sifre Degistir
              </h3>
              <form onSubmit={handlePasswordChange} className="space-y-4">
                <div>
                  <label className="text-xs text-muted-foreground mb-1.5 block">Mevcut Sifre</label>
                  <div className="relative">
                    <Lock size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
                    <Input
                      type="password"
                      value={passwordForm.current_password}
                      onChange={(e) => setPasswordForm((f) => ({ ...f, current_password: e.target.value }))}
                      className="pl-9"
                      placeholder="Mevcut sifreniz"
                    />
                  </div>
                </div>
                <div>
                  <label className="text-xs text-muted-foreground mb-1.5 block">Yeni Sifre (min. 6 karakter)</label>
                  <div className="relative">
                    <Lock size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
                    <Input
                      type="password"
                      value={passwordForm.new_password}
                      onChange={(e) => setPasswordForm((f) => ({ ...f, new_password: e.target.value }))}
                      className="pl-9"
                      placeholder="Yeni sifreniz"
                    />
                  </div>
                </div>
                <div>
                  <label className="text-xs text-muted-foreground mb-1.5 block">Yeni Sifre (Tekrar)</label>
                  <div className="relative">
                    <Lock size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
                    <Input
                      type="password"
                      value={passwordForm.confirm_password}
                      onChange={(e) => setPasswordForm((f) => ({ ...f, confirm_password: e.target.value }))}
                      className="pl-9"
                      placeholder="Yeni sifrenizi tekrar girin"
                    />
                  </div>
                </div>
                {passwordMsg.text && (
                  <p className={`text-sm ${passwordMsg.type === "success" ? "text-green-400" : "text-red-400"}`}>
                    {passwordMsg.text}
                  </p>
                )}
                <Button type="submit" disabled={passwordSaving} variant="outline" className="w-full">
                  <Lock size={14} className="mr-2" /> {passwordSaving ? "Degistiriliyor..." : "Sifreyi Degistir"}
                </Button>
              </form>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </div>
  );
}
