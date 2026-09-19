"use client";

import { useState, useEffect, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import AppShell from "./components/layout/AppShell";
import CaseWizard from "./components/cases/CaseWizard";
import CitizenIngestionWizard from "./components/cases/CitizenIngestionWizard";
import CaseWorkspace from "./components/cases/CaseWorkspace";
import LandingPage from "./components/landing/LandingPage";
import PortalAuthPage, { LeaOfficerDetails } from "./components/auth/PortalAuthPage";

type AppView = "landing" | "auth" | "app";
type UserRole = "citizen" | "lea";

function HomeContent() {
  const searchParams = useSearchParams();
  const [currentView, setCurrentView] = useState<AppView>("landing");
  const [userRole, setUserRole] = useState<UserRole>("lea");
  const [officerDetails, setOfficerDetails] = useState<LeaOfficerDetails | undefined>(undefined);
  
  const [activeCase, setActiveCase] = useState<{
    caseId: string;
    seedAddress: string;
    firNumber?: string;
    ioDesignation?: string;
  } | null>(null);
  
  const [currentStep, setCurrentStep] = useState<number>(1);

  useEffect(() => {
    const caseId = searchParams?.get('caseId');
    const seedAddress = searchParams?.get('seedAddress') || '';
    
    if (caseId) {
      setActiveCase({ caseId, seedAddress });
      setCurrentView("app");
    }
  }, [searchParams]);

  // View 1: Landing Page with Video Scrubbing
  if (currentView === "landing") {
    return <LandingPage onLaunch={() => setCurrentView("auth")} />;
  }

  // View 2: Portal Selection / Login Screen (Citizen vs LEA)
  if (currentView === "auth") {
    return (
      <PortalAuthPage
        onBackToLanding={() => setCurrentView("landing")}
        onSelectCitizen={() => {
          setUserRole("citizen");
          setActiveCase(null);
          setCurrentStep(1);
          setCurrentView("app");
        }}
        onSelectLea={(officer) => {
          setUserRole("lea");
          setOfficerDetails(officer);
          setActiveCase(null);
          setCurrentStep(1);
          setCurrentView("app");
        }}
      />
    );
  }

  // View 3: App Workspace (Citizen Rapid Ingestion OR LEA 3-Step Wizard OR Live Graph Workspace)
  return (
    <AppShell 
      currentStep={currentStep} 
      onStepChange={(step) => setCurrentStep(step)}
      activeCase={activeCase}
      userRole={userRole}
      officerDetails={officerDetails}
      onSwitchPortal={() => {
        setActiveCase(null);
        setCurrentView("auth");
      }}
    >
      {!activeCase ? (
        userRole === "citizen" ? (
          /* Citizen Direct Seed Wallet Ingestion (Bypasses FIR, Station, IO, etc.) */
          <CitizenIngestionWizard
            onBackToPortal={() => {
              setActiveCase(null);
              setCurrentView("auth");
            }}
            onComplete={async (caseId, seedAddress, disputedAmount, incidentType) => {
              try {
                const res = await fetch('http://localhost:8000/api/v1/cases/', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({
                    case_id: caseId,
                    authority: 'Citizen Ingestion',
                    seed_address: seedAddress,
                    fir_number: '',
                    io_designation: 'N/A (Citizen Ingestion)',
                    police_station: '',
                    jurisdiction_bench: '',
                    disputed_value_inr: disputedAmount || ''
                  })
                });
                if (!res.ok) console.error("Failed to create citizen case");
              } catch (err) {
                console.error("API error creating citizen case", err);
              }
              setActiveCase({ caseId, seedAddress, firNumber: '', ioDesignation: 'N/A (Citizen Ingestion)' });
              setCurrentStep(4);
            }}
          />
        ) : (
          /* LEA 3-Step Legal & Statutory Case Initialization Wizard */
          <CaseWizard 
            currentStep={currentStep as 1 | 2 | 3}
            onStepChange={(step) => setCurrentStep(step)}
            initialOfficerDetails={officerDetails}
            onBackToPortal={() => {
              setActiveCase(null);
              setCurrentView("auth");
            }}
            onComplete={async (caseId, seedAddress, firNumber, ioDesignation, statuteRef, policeStation, jurisdictionBench, disputedAmount) => {
              try {
                const res = await fetch('http://localhost:8000/api/v1/cases/', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({
                    case_id: caseId,
                    authority: statuteRef,
                    seed_address: seedAddress,
                    fir_number: firNumber,
                    io_designation: ioDesignation,
                    police_station: policeStation,
                    jurisdiction_bench: jurisdictionBench,
                    disputed_value_inr: disputedAmount
                  })
                });
                if (!res.ok) console.error("Failed to create LEA case");
              } catch (err) {
                console.error("API error creating LEA case", err);
              }
              setActiveCase({ caseId, seedAddress, firNumber, ioDesignation });
              setCurrentStep(4);
            }} 
          />
        )
      ) : (
        /* Live Graph Resolution, Attributed Path, & Cryptographic Dossier Workspace */
        <CaseWorkspace 
          caseId={activeCase.caseId} 
          seedAddress={activeCase.seedAddress} 
        />
      )}
    </AppShell>
  );
}

export default function Home() {
  return (
    <Suspense fallback={<div className="flex items-center justify-center min-h-screen bg-slate-900 text-white font-mono text-xs">Loading PHANTASM Suite...</div>}>
      <HomeContent />
    </Suspense>
  );
}
