import {useEffect,useState} from 'react'
import {ArrowUpRight,ChevronRight} from 'lucide-react'
import {listApplications,getApplication} from '../services/api'
import type {Application,CaseDetail} from '../types/application'
import {MetricCard} from '../components/MetricCard'
import {CaseDrawer} from '../components/CaseDrawer'
export function Dashboard(){
 const [apps,setApps]=useState<Application[]>([]);const [selected,setSelected]=useState<CaseDetail|null>(null)
 useEffect(()=>{listApplications().then(setApps).catch(()=>setApps([]))},[])
 const open=async(id:string)=>setSelected(await getApplication(id))
 return <main className="p-5 md:p-8 max-w-7xl mx-auto w-full">
  <header className="flex flex-col sm:flex-row sm:items-center justify-between gap-5 mb-7"><div><div className="text-[11px] uppercase tracking-[.18em] text-zinc-400">Government services · Sandbox</div><h1 className="text-3xl font-bold tracking-tight mt-1">Application Rescue</h1><p className="text-sm text-zinc-500 mt-1">Resolve correctable application issues by voice.</p></div><button onClick={()=>open('APP-004281')} className="bg-zinc-950 text-white rounded-xl px-4 py-2.5 text-sm font-semibold flex items-center gap-2">View priority case<ArrowUpRight size={15}/></button></header>
  <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-5"><MetricCard value={String(apps.length)} label="Application exceptions"/><MetricCard value="—" label="Calls completed"/><MetricCard value="—" label="Corrections resolved"/><MetricCard value="—" label="Human escalations"/></div>
  <section className="bg-white border border-zinc-200 rounded-2xl overflow-hidden"><div className="p-5 border-b border-zinc-100 flex justify-between"><h2 className="font-semibold text-sm">Recent application exceptions</h2><span className="text-[11px] px-2 py-1 rounded-full bg-emerald-50 text-emerald-700 font-bold">Backend connected</span></div>
   <div className="overflow-x-auto"><table className="w-full text-sm"><thead><tr className="text-[10px] uppercase tracking-wider text-zinc-400 border-b border-zinc-100"><th className="text-left p-4 pl-5">Application</th><th className="text-left p-4">Service</th><th className="text-left p-4">Issue</th><th className="text-left p-4">Status</th><th></th></tr></thead>
   <tbody>{apps.map(a=><tr key={a.id} onClick={()=>open(a.id)} className="border-b border-zinc-100 hover:bg-zinc-50 cursor-pointer"><td className="p-4 pl-5"><b>{a.id}</b><div className="text-xs text-zinc-400">{a.applicant} · {a.language}</div></td><td className="p-4">{a.service}</td><td className="p-4">{a.issue}</td><td className="p-4"><span className="px-2 py-1 rounded-full text-[11px] font-bold bg-amber-50 text-amber-700">{a.status}</span></td><td className="p-4"><ChevronRight size={15} className="text-zinc-400"/></td></tr>)}</tbody></table></div>
  </section><CaseDrawer data={selected} onClose={()=>setSelected(null)}/>
 </main>}