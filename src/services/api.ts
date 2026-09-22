import type {Application,CaseDetail} from '../types/application'

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api'

async function request<T>(path:string, init?:RequestInit):Promise<T>{
 const res=await fetch(`${API_BASE}${path}`,{headers:{'Content-Type':'application/json',...(init?.headers||{})},...init})
 const data=await res.json()
 if(!res.ok){ const detail=typeof data?.detail==='string'?data.detail:data?.detail?.message||data?.detail?.code; throw new Error(detail||data?.error?.message||`Request failed: ${res.status}`) }
 return data
}

export async function listApplications():Promise<Application[]>{
 const data=await request<any[]>('/applications')
 return data.map(c=>({id:c.id,applicant:c.applicant,language:c.language,service:c.service,issue:c.issue,status:mapStatus(c.status)}))
}

export async function getApplication(id:string):Promise<CaseDetail>{
 const c=await request<any>(`/applications/${id}`)
 return {...c,id:c.id,applicant:c.applicant,language:c.language,service:c.service,issue:c.issue,status:mapStatus(c.status),allowedAction:c.allowed_actions?.[0]??null,blockedActions:['approve_application','reject_application','change_final_decision']}
}

export async function verifyApplication(id:string):Promise<any>{
 return request('/verify',{method:'POST',body:JSON.stringify({application_id:id,challenge_passed:true})})
}

export async function checkPolicy(id:string,action:string,consent:boolean):Promise<any>{
 return request('/policy/check',{method:'POST',body:JSON.stringify({application_id:id,action,consent,idempotency_key:`policy-${id}-${Date.now()}`})})
}

export async function executeAction(id:string,action:string):Promise<any>{
 return request('/actions/execute',{method:'POST',body:JSON.stringify({application_id:id,action,consent:true,idempotency_key:`demo-${id}-${Date.now()}`})})
}

function mapStatus(status:string):Application['status']{
 if(status==='APPOINTMENT_REQUIRED') return 'appointment'
 if(status==='DISPUTE') return 'escalated'
 if(status==='CORRECTION_SUBMITTED') return 'submitted'
 return 'correction'
}


export async function getElevenLabsSignedUrl(): Promise<string>{
 const data = await request<{signedUrl:string}>('/elevenlabs/signed-url')
 return data.signedUrl
}


export async function startOutboundCall(applicationId:string,toNumber:string,callRecordingEnabled=true):Promise<any>{
 return request('/outbound-call',{
   method:'POST',
   body:JSON.stringify({
     application_id:applicationId,
     to_number:toNumber,
     call_recording_enabled:callRecordingEnabled
   })
 })
}
