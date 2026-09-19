"use client";

import { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation";
import AppShell from "./components/layout/AppShell";
import CaseWizard from "./components/cases/CaseWizard";
import CaseWorkspace from "./components/cases/CaseWorkspace";

export default function Home() {
  const searchParams = useSearchParams();
  const [activeCase, setActiveCase] = useState<{caseId: string, seedAddress: string} | null>(null);

  useEffect(() => {
    const caseId = searchParams?.get('caseId');
    const seedAddress = searchParams?.get('seedAddress') || 'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh'; // fallback for demo if missing
    
    if (caseId) {
      setActiveCase({ caseId, seedAddress });
    }
  }, [searchParams]);

  return (
    <AppShell>
      {!activeCase ? (
        <CaseWizard onComplete={(caseId, seedAddress) => setActiveCase({ caseId, seedAddress })} />
      ) : (
        <CaseWorkspace caseId={activeCase.caseId} seedAddress={activeCase.seedAddress} />
      )}
    </AppShell>
  );
}
