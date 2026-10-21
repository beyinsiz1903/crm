import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Bell, Check, CheckCheck, Info, AlertTriangle, CheckCircle, XCircle } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import PageHeader from "@/components/PageHeader";
import { getNotifications, markNotificationRead, markAllNotificationsRead } from "@/lib/api";

const typeIcons = {
  info: <Info size={16} className="text-blue-400" />,
  success: <CheckCircle size={16} className="text-green-400" />,
  warning: <AlertTriangle size={16} className="text-yellow-400" />,
  error: <XCircle size={16} className="text-red-400" />,
};

export default function Notifications() {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);

  const load = () => {
    setLoading(true);
    getNotifications()
      .then(setNotifications)
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, []);

  const handleMarkRead = async (id) => {
    await markNotificationRead(id);
    setNotifications((prev) => prev.map((n) => (n.id === id ? { ...n, read: true } : n)));
  };

  const handleMarkAllRead = async () => {
    await markAllNotificationsRead();
    setNotifications((prev) => prev.map((n) => ({ ...n, read: true })));
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return "";
    const d = new Date(dateStr);
    const now = new Date();
    const diffMs = now - d;
    const diffMin = Math.floor(diffMs / 60000);
    if (diffMin < 1) return "az once";
    if (diffMin < 60) return `${diffMin} dk once`;
    const diffH = Math.floor(diffMin / 60);
    if (diffH < 24) return `${diffH} saat once`;
    const diffD = Math.floor(diffH / 24);
    if (diffD < 7) return `${diffD} gun once`;
    return d.toLocaleDateString("tr-TR");
  };

  const unreadCount = notifications.filter((n) => !n.read).length;

  if (loading) {
    return (
      <div className="page-content">
        <div className="animate-pulse space-y-4">
          <div className="h-8 w-48 bg-muted rounded" />
          {[1, 2, 3].map((i) => (<div key={i} className="h-20 bg-muted rounded-xl" />))}
        </div>
      </div>
    );
  }

  return (
    <div className="page-content">
      <div className="flex items-center justify-between mb-6">
        <PageHeader title="Bildirimler" subtitle={`${unreadCount} okunmamis bildirim`} />
        {unreadCount > 0 && (
          <Button variant="outline" size="sm" onClick={handleMarkAllRead}>
            <CheckCheck size={14} className="mr-2" /> Tumunu Okundu Isaretle
          </Button>
        )}
      </div>

      {notifications.length === 0 ? (
        <Card>
          <CardContent className="p-12 text-center">
            <Bell size={48} className="mx-auto text-muted-foreground mb-4 opacity-30" />
            <p className="text-muted-foreground">Henuz bildirim yok</p>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-2">
          {notifications.map((notif, i) => (
            <motion.div
              key={notif.id}
              initial={{ opacity: 0, y: 5 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.03 }}
            >
              <Card className={`transition-colors ${!notif.read ? "border-primary/30 bg-primary/5" : "opacity-70"}`}>
                <CardContent className="p-4 flex items-start gap-3">
                  <div className="mt-0.5">
                    {typeIcons[notif.type] || typeIcons.info}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="font-medium text-sm">{notif.title}</span>
                      {!notif.read && <Badge variant="secondary" className="text-[10px] bg-primary/20 text-primary">Yeni</Badge>}
                    </div>
                    <p className="text-sm text-muted-foreground">{notif.message}</p>
                    <p className="text-[10px] text-muted-foreground mt-1">{formatDate(notif.created_at)}</p>
                  </div>
                  {!notif.read && (
                    <Button variant="ghost" size="sm" onClick={() => handleMarkRead(notif.id)} className="shrink-0">
                      <Check size={14} />
                    </Button>
                  )}
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}
