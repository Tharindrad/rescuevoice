import {X,PhoneCall,Check,ShieldAlert,UserCheck,MessageSquare,LockKeyhole,Loader2,AlertTriangle} from 'lucide-react'
import type {CaseDetail} from '../types/application'
import {checkPolicy,executeAction,verifyApplication,startOutboundCall} from '../services/api'
import {useState} from 'react'
import {VoiceCall} from './VoiceCall'

type Step={id:string;label:string;detail:string;state:'pending'|'active'|'done'|'blocked'}

export function CaseDrawer({data,onClose}:{data:CaseDetail|null;onClose:()=>void}){
 const [running,setRunning]=useState(false); const [step,setStep]=useState(0); const [result,setResult]=useState<any>(null); const [error,setError]=useState(''); const [voiceOpen,setVoiceOpen]=useState(false); const [outboundNumber,setOutboundNumber]=useState(''); const [callResult,setCallResult]=useState<any>(null); const [calling,setCalling]=useState(false)
 if(!data)return null
 const steps:Step[]=[
  {id:'call',label:'Identify',detail:'AI disclosure + preferred language',state:step>0?'done':step===0?'active':'pending'},
  {id:'verify',label:'Verify',detail:'Approved challenge verification',state:step>1?'done':step===1?'active':'pending'},
  {id:'explain',label:'Explain',detail:'Read the recorded application issue',state:step>2?'done':step===2?'active':'pending'},
  {id:'consent',label:'Consent',detail:'Explicit permission for state change',state:step>3?'done':step===3?'active':'pending'},
  {id:'policy',label:'Policy Gate',detail:'Server-side action authorization',state:step>4?'done':step===4?'active':'pending'},
  {id:'action',label:'Action',detail:'Execute only the approved remediation',state:step>5?'done':step===5?'active':'pending'},
  {id:'audit',label:'Human Review + Audit',detail:'Final decision stays with authority officer',state:step>6?'done':step===6?'active':'pending'},
 ]
 const start=async()=>{
  setRunning(true);setError('');setResult(null)
  try{
   setStep(0);await wait(450);setStep(1)
   const v=await verifyApplication(data.id);if(!v.verified) throw new Error('Verification failed')
   await wait(500);setStep(2);await wait(700);setStep(3);await wait(700);setStep(4)
   if(!data.allowedAction) throw new Error('No permitted remediation exists; case requires human escalation.')
   const policy=await checkPolicy(data.id,data.allowedAction,true)
   if(!policy.allowed) throw new Error(policy.reason||'Policy gate blocked action')
   await wait(500);setStep(5)
   const action=await executeAction(data.id,data.allowedAction)
   if(!action.ok) throw new Error(action.error?.message||'Government action failed')
   setResult(action);await wait(500);setStep(6);await wait(500);setStep(7)
  }catch(e:any){setError(e.message||'Flow stopped safely');setStep(4)}finally{setRunning(false)}
 }
 return <div className="fixed inset-0 bg-black/25 flex justify-end z-20" onClick={e=>e.target===e.currentTarget&&onClose()}>
  <div className="w-full max-w-2xl bg-white h-full p-6 overflow-auto shadow-2xl">
   <div className="flex justify-between items-center"><div><span className="text-[11px] uppercase tracking-widest text-zinc-400">Live operations · Sandbox</span><div className="text-2xl font-bold mt-1">{data.id}</div></div><button onClick={onClose} className="p-2 rounded-full bg-zinc-100"><X size={16}/></button></div>
   <div className="text-sm text-zinc-500 mt-1">{data.service} · {data.applicant} · {data.language}</div>
   <div className="mt-6 grid grid-cols-2 gap-3"><Info label="Issue" value={data.issue}/><Info label="Allowed action" value={data.allowedAction||'Human escalation'}/></div>
   <div className="mt-6 border border-zinc-200 rounded-2xl overflow-hidden">
    <div className="p-4 border-b bg-zinc-50 flex justify-between items-center"><div><b className="text-sm">Rescue call workflow</b><p className="text-xs text-zinc-500 mt-1">Harness-controlled simulation; no real call yet.</p></div>{running?<Loader2 className="animate-spin" size={18}/>:<PhoneCall size={18}/>}</div>
    <div className="p-4 space-y-2">{steps.map((s,i)=><div key={s.id} className={`flex gap-3 items-start p-3 rounded-xl ${s.state==='active'?'bg-zinc-100':''}`}><div className={`w-7 h-7 rounded-full grid place-items-center text-xs font-bold ${s.state==='done'?'bg-emerald-100 text-emerald-700':s.state==='active'?'bg-zinc-950 text-white':s.state==='blocked'?'bg-red-100 text-red-700':'bg-zinc-100 text-zinc-400'}`}>{s.state==='done'?<Check size={14}/>:i+1}</div><div className="flex-1"><b className="text-sm">{s.label}</b><p className="text-xs text-zinc-500 mt-0.5">{s.detail}</p></div></div>)}</div>
   </div>
   <div className="mt-5 grid grid-cols-2 gap-3"><Guard icon={<UserCheck size={15}/>} title="Verification" text="Required before action"/><Guard icon={<LockKeyhole size={15}/>} title="Consent" text="Required before state change"/><Guard icon={<ShieldAlert size={15}/>} title="Policy gate" text="Server-side allow-list"/><Guard icon={<MessageSquare size={15}/>} title="Final decision" text="Human officer"/></div>
   {callResult&&<div className="mt-4 p-4 rounded-2xl bg-emerald-50 text-emerald-800 text-sm"><b>Outbound call started</b><div className="text-xs mt-1">Call SID: {callResult.call_sid||'pending'} · Conversation: {callResult.conversation_id||'pending'}</div></div>}
   {error&&<div className="mt-5 p-4 rounded-2xl bg-red-50 text-red-700 text-sm flex gap-2"><AlertTriangle size={17}/><div><b>Flow stopped safely</b><div className="text-xs mt-1">{error}</div></div></div>}
   {result&&<div className="mt-5 p-4 rounded-2xl bg-emerald-50 text-emerald-800 text-sm"><b className="flex gap-2 items-center"><Check size={17}/> Correction submitted</b><div className="text-xs mt-1">Status: {result.status}. Final decision remains with {result.final_decision_owner||'the authority officer'}.</div></div>}
   <div className="mt-5 p-4 rounded-2xl bg-zinc-50 border border-zinc-200">
     <div className="text-[10px] uppercase tracking-wider text-zinc-400">Twilio outbound · test only</div>
     <div className="flex gap-2 mt-2">
       <input value={outboundNumber} onChange={e=>setOutboundNumber(e.target.value)} placeholder="+9715XXXXXXXX" className="flex-1 px-3 py-2.5 rounded-xl border border-zinc-200 text-sm outline-none focus:ring-2 focus:ring-zinc-200"/>
       <button disabled={calling||!outboundNumber} onClick={async()=>{setCalling(true);setError('');setCallResult(null);try{const r=await startOutboundCall(data.id,outboundNumber,true);setCallResult(r)}catch(e:any){setError(e.message||'Outbound call failed')}finally{setCalling(false)}}} className="px-4 py-2.5 rounded-xl bg-zinc-950 text-white text-sm font-semibold disabled:bg-zinc-300">{calling?'Calling…':'Call applicant'}</button>
     </div>
     <p className="text-[11px] text-zinc-500 mt-2">Requires ElevenLabs native Twilio integration and a configured agent phone number ID.</p>
    </div>
    
{!running&&!result&&<div className="mt-6 grid grid-cols-2 gap-3"><button disabled={!data.allowedAction} onClick={()=>setVoiceOpen(true)} className="bg-zinc-950 disabled:bg-zinc-300 text-white py-3.5 rounded-xl font-semibold flex items-center justify-center gap-2"><PhoneCall size={17}/> Live voice</button><button disabled={!data.allowedAction} onClick={start} className="border border-zinc-200 disabled:text-zinc-300 text-zinc-900 py-3.5 rounded-xl font-semibold">Simulate flow</button></div>}
  </div></div>
}
function Info({label,value}:{label:string,value:string}){return <div className="p-4 rounded-2xl bg-zinc-50"><div className="text-[10px] uppercase tracking-wider text-zinc-400">{label}</div><div className="text-sm font-semibold mt-1">{value}</div></div>}
function Guard({icon,title,text}:{icon:any,title:string,text:string}){return <div className="border border-zinc-200 rounded-xl p-3 flex gap-2 items-start"><div className="mt-0.5">{icon}</div><div><b className="text-xs">{title}</b><p className="text-[11px] text-zinc-500">{text}</p></div></div>}
function wait(ms:number){return new Promise(r=>setTimeout(r,ms))}
