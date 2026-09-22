import {LayoutDashboard,FileText,Phone,CalendarDays,ShieldCheck} from 'lucide-react'
export function Sidebar({active,setActive}:{active:string;setActive:(x:string)=>void}){
 const items=[['Overview',LayoutDashboard],['Applications',FileText],['Calls',Phone],['Appointments',CalendarDays],['Audit',ShieldCheck]]
 return <aside className="hidden md:flex w-56 shrink-0 bg-white border-r border-zinc-200 p-5 flex-col min-h-screen">
  <div className="font-extrabold text-xl tracking-tight px-2 pb-8">Rescue<span className="font-medium text-zinc-500">Voice</span></div>
  <nav className="space-y-1">{items.map(([name,Icon])=><button key={name as string} onClick={()=>setActive(name as string)} className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm ${active===name?'bg-zinc-100 text-zinc-950 font-semibold':'text-zinc-500 hover:bg-zinc-50'}`}><Icon size={16}/>{name as string}</button>)}</nav>
  <div className="mt-auto text-xs text-zinc-500 px-2"><span className="inline-block w-2 h-2 rounded-full bg-emerald-500 mr-2"/>Sandbox connected</div>
 </aside>}