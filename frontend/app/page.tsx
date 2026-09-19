import AppShell from "./components/layout/AppShell";
import CaseWizard from "./components/cases/CaseWizard";

export default function Home() {
  return (
    <AppShell>
      <CaseWizard />
    </AppShell>
  );
}
