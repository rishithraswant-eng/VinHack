"use client";
import {Suspense} from 'react';
import {useSearchParams} from 'next/navigation';
import Script from 'next/script';
import AppShell from '../components/layout/AppShell';
import CaseWizard from '../components/cases/CaseWizard';
import CaseWorkspace from '../components/cases/CaseWorkspace';
import LoginForm from '../components/auth/LoginForm';
import AuditExplorer from '../components/audit/AuditExplorer';
import SignOffPanel from '../components/supervisor/SignOffPanel';
import BlockchainGraph from '../components/cases/BlockchainGraph';
import PreviewWorkspace from './PreviewWorkspace';
function Preview(){
 const q=useSearchParams(); const view=q.get('view')||'step1';
 const seed='0x0000000000000000000000000000000000000000';
 if(view==='all') return <><div id="figma-source" style={{width:1440,display:'flex',flexDirection:'column',gap:80,background:'#e2e8f0'}}>
 <section aria-label="01 Landing" data-screen="01 Landing" style={{height:900,position:'relative',background:'#000',color:'white',display:'flex',alignItems:'center',justifyContent:'center'}}><div style={{border:'1px dashed #64748b',padding:80,textAlign:'center'}}><h1 style={{fontSize:48,fontWeight:700}}>PHANTASM</h1><p style={{fontSize:20,marginTop:16}}>Scroll-controlled video / landing.mp4</p></div><button className="absolute bottom-16 px-10 py-4 rounded-full font-semibold text-lg tracking-widest text-white uppercase bg-blue-600/20 border border-blue-400/40">Launch Forensic Suite</button></section>
 <section aria-label="02 Secure Login" data-screen="02 Secure Login"><LoginForm/></section>
 {[1,2,3].map(step=><section key={step} aria-label={`0${step+2} Case Setup Step ${step}`} data-screen={`0${step+2} Case Setup Step ${step}`}><AppShell currentStep={step}><CaseWizard currentStep={step as 1|2|3}/></AppShell></section>)}
 <section aria-label="06 Investigation Workspace" data-screen="06 Investigation Workspace"><AppShell activeCase={{caseId:'PHT-DEMO',seedAddress:seed}}><PreviewWorkspace caseId="PHT-DEMO" seedAddress={seed}/></AppShell></section>
 <section aria-label="07 Completed Investigation" data-screen="07 Completed Investigation"><AppShell activeCase={{caseId:'PHT-DEMO',seedAddress:seed}}><PreviewWorkspace caseId="PHT-DEMO" seedAddress={seed} previewState="COMPLETED"/></AppShell></section>
 <section aria-label="08 Expanded Graph" data-screen="08 Expanded Graph" style={{height:900}}><BlockchainGraph caseId="PHT-DEMO" seedAddress={seed} traceState="COMPLETED" traceResult={{confidence:0.806,vasp_node:'vasp_exchange_dynamic'}}/></section>
 <section aria-label="09 Audit Explorer" data-screen="09 Audit Explorer"><AuditExplorer/></section>
 <section aria-label="10 Supervisor Sign-Off" data-screen="10 Supervisor Sign-Off" className="min-h-screen bg-slate-900 flex items-center justify-center"><SignOffPanel confidenceScore={0.806} recipientDesignation="Nodal Officer, VASP" onSignOff={()=>{}}/></section>
 </div><Script src="https://mcp.figma.com/mcp/html-to-design/capture.js" strategy="afterInteractive"/></>;
 return <><div id="figma-source" style={{width:1440,minHeight:900}}>
 {view.startsWith('step')?<AppShell currentStep={Number(view.slice(-1))}><CaseWizard currentStep={Number(view.slice(-1)) as 1|2|3}/></AppShell>:
 view==='login'?<LoginForm/>:view==='audit'?<AuditExplorer/>:view==='signoff'?<div className="min-h-screen bg-slate-900 flex items-center justify-center"><SignOffPanel confidenceScore={0.806} recipientDesignation="Nodal Officer, VASP" onSignOff={()=>{}}/></div>:
 view==='graph'?<div style={{height:900}}><BlockchainGraph caseId="PHT-DEMO" seedAddress={seed} traceState="COMPLETED" traceResult={{confidence:0.806,vasp_node:'vasp_exchange_dynamic'}}/></div>:
 <AppShell activeCase={{caseId:'PHT-DEMO',seedAddress:seed}}><CaseWorkspace caseId="PHT-DEMO" seedAddress={seed}/></AppShell>}
 </div><Script src="https://mcp.figma.com/mcp/html-to-design/capture.js" strategy="afterInteractive"/></>;
}
export default function Page(){return <Suspense><Preview/></Suspense>}
