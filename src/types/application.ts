export type ApplicationStatus='correction'|'appointment'|'escalated'|'resolved'|'submitted'
export interface Application {id:string; applicant:string; language:string; service:string; issue:string; status:ApplicationStatus}
export interface CaseDetail extends Application {allowedAction:string|null; blockedActions:string[]; final_decision_owner:string}
