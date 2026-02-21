import { useState, useEffect, useCallback } from "react";
import { DndContext, closestCenter, PointerSensor, useSensor, useSensors, DragOverlay } from "@dnd-kit/core";
import { SortableContext, verticalListSortingStrategy, useSortable } from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";
import { motion } from "framer-motion";
import { GripVertical, User, Star, Building2, Mail, Phone } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import PageHeader from "@/components/PageHeader";
import { getPipelineBoard, updateLeadStage, getLeads } from "@/lib/api";

const STAGE_COLORS = {
  new: { bg: "bg-blue-500/10", border: "border-blue-500/30", text: "text-blue-600", dot: "bg-blue-500" },
  contacted: { bg: "bg-yellow-500/10", border: "border-yellow-500/30", text: "text-yellow-600", dot: "bg-yellow-500" },
  qualified: { bg: "bg-orange-500/10", border: "border-orange-500/30", text: "text-orange-600", dot: "bg-orange-500" },
  proposal: { bg: "bg-purple-500/10", border: "border-purple-500/30", text: "text-purple-600", dot: "bg-purple-500" },
  negotiation: { bg: "bg-indigo-500/10", border: "border-indigo-500/30", text: "text-indigo-600", dot: "bg-indigo-500" },
  won: { bg: "bg-green-500/10", border: "border-green-500/30", text: "text-green-600", dot: "bg-green-500" },
  lost: { bg: "bg-red-500/10", border: "border-red-500/30", text: "text-red-600", dot: "bg-red-500" },
};

function LeadCard({ lead, isDragging }) {
  const scoreColor = lead.score >= 70 ? "text-green-500" : lead.score >= 40 ? "text-yellow-500" : "text-red-400";
  return (
    <div className={`p-3 bg-card rounded-lg border border-border shadow-sm ${isDragging ? 'opacity-50 shadow-lg' : 'hover:shadow-md'} transition-all cursor-grab`}>
      <div className="flex justify-between items-start mb-2">
        <div className="font-medium text-sm truncate flex-1">{lead.name}</div>
        <span className={`text-xs font-bold ${scoreColor} ml-2`}>{lead.score}</span>
      </div>
      {lead.company && <div className="flex items-center gap-1 text-xs text-muted-foreground mb-1"><Building2 size={10} />{lead.company}</div>}
      {lead.email && <div className="flex items-center gap-1 text-xs text-muted-foreground mb-1"><Mail size={10} /><span className="truncate">{lead.email}</span></div>}
      <div className="flex gap-1 mt-2 flex-wrap">
        {(lead.tags || []).slice(0, 2).map((t) => <Badge key={t} variant="secondary" className="text-[9px] px-1.5 py-0">{t}</Badge>)}
        <Badge variant="outline" className="text-[9px] px-1.5 py-0">
          {["website","referral","social","direct","ad","event","other"].includes(lead.source) ? ({website:"Web",referral:"Ref",social:"Sosyal",direct:"Direkt",ad:"Reklam",event:"Etkinlik",other:"Diger"})[lead.source] : lead.source}
        </Badge>
      </div>
    </div>
  );
}

function DraggableLeadCard({ lead }) {
  const { attributes, listeners, setNodeRef, transform, transition, isDragging } = useSortable({ id: lead.id, data: { lead } });
  const style = { transform: CSS.Transform.toString(transform), transition };
  return (
    <div ref={setNodeRef} style={style} {...attributes} {...listeners}>
      <LeadCard lead={lead} isDragging={isDragging} />
    </div>
  );
}

export default function Pipeline() {
  const [board, setBoard] = useState({});
  const [leads, setLeads] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeLead, setActiveLead] = useState(null);

  const sensors = useSensors(
    useSensor(PointerSensor, { activationConstraint: { distance: 5 } })
  );

  const load = useCallback(() => {
    setLoading(true);
    Promise.all([getPipelineBoard(), getLeads({})]).then(([boardData, leadsData]) => {
      setBoard(boardData);
      setLeads(leadsData);
    }).catch(console.error).finally(() => setLoading(false));
  }, []);

  useEffect(() => { load(); }, [load]);

  const stageOrder = ["new", "contacted", "qualified", "proposal", "negotiation", "won", "lost"];
  const stageNames = { new: "Yeni", contacted: "Iletisime Gecildi", qualified: "Nitelikli", proposal: "Teklif", negotiation: "Muzakere", won: "Kazanildi", lost: "Kaybedildi" };

  const getLeadsByStage = (stageKey) => {
    if (board[stageKey]?.leads) return board[stageKey].leads;
    return leads.filter((l) => l.stage === stageKey);
  };

  const handleDragStart = (event) => {
    const lead = leads.find((l) => l.id === event.active.id) || event.active.data?.current?.lead;
    setActiveLead(lead);
  };

  const handleDragEnd = async (event) => {
    setActiveLead(null);
    const { active, over } = event;
    if (!over || !active) return;

    const draggedLead = leads.find((l) => l.id === active.id);
    if (!draggedLead) return;

    // Find target stage
    let targetStage = null;
    // Check if dropped over a stage column
    for (const sk of stageOrder) {
      const stageLeads = getLeadsByStage(sk);
      if (over.id === `stage-${sk}` || stageLeads.some((l) => l.id === over.id)) {
        targetStage = sk;
        break;
      }
    }
    // Also check if over.id matches a stage droppable
    if (!targetStage && typeof over.id === 'string' && over.id.startsWith('stage-')) {
      targetStage = over.id.replace('stage-', '');
    }

    if (targetStage && targetStage !== draggedLead.stage) {
      try {
        await updateLeadStage(draggedLead.id, targetStage);
        load();
      } catch (err) { console.error(err); }
    }
  };

  if (loading) return <div className="page-content"><div className="animate-pulse space-y-4"><div className="h-8 w-48 bg-muted rounded" /><div className="flex gap-4">{[1,2,3,4,5].map(i => <div key={i} className="flex-1 h-96 bg-muted rounded-xl" />)}</div></div></div>;

  return (
    <div className="page-content">
      <PageHeader title="Satis Hunisi" subtitle="Lead'lerinizi surukle-birak ile yonetin" />

      <DndContext sensors={sensors} collisionDetection={closestCenter} onDragStart={handleDragStart} onDragEnd={handleDragEnd}>
        <div className="flex gap-4 overflow-x-auto pb-4" style={{ minHeight: '500px' }}>
          {stageOrder.map((stageKey) => {
            const colors = STAGE_COLORS[stageKey] || STAGE_COLORS.new;
            const stageLeads = getLeadsByStage(stageKey);
            return (
              <SortableContext key={stageKey} items={stageLeads.map(l => l.id)} strategy={verticalListSortingStrategy} id={`stage-${stageKey}`}>
                <div className={`flex-shrink-0 w-[240px] rounded-xl ${colors.bg} border ${colors.border} p-3`}>
                  <div className="flex items-center gap-2 mb-3">
                    <div className={`w-2.5 h-2.5 rounded-full ${colors.dot}`} />
                    <span className={`text-sm font-semibold ${colors.text}`}>{stageNames[stageKey]}</span>
                    <Badge variant="secondary" className="text-[10px] ml-auto">{stageLeads.length}</Badge>
                  </div>
                  <div className="space-y-2 min-h-[200px]">
                    {stageLeads.map((lead) => <DraggableLeadCard key={lead.id} lead={lead} />)}
                    {stageLeads.length === 0 && <div className="text-center text-xs text-muted-foreground py-8">Bos</div>}
                  </div>
                </div>
              </SortableContext>
            );
          })}
        </div>
        <DragOverlay>{activeLead ? <LeadCard lead={activeLead} isDragging /> : null}</DragOverlay>
      </DndContext>
    </div>
  );
}
