"use client";

import { useState } from "react";

type AuditLog = {
  id: string;
  userId: string;
  role: string;
  action: string;
  targetCase: string;
  timestamp: string;
  integrityValid: boolean;
};

const MOCK_LOGS: AuditLog[] = [
  { id: "A-1092", userId: "IO-10492", role: "OFFICER", action: "POST /cases/123/trace", targetCase: "CASE-123", timestamp: "2026-09-01T10:23:44Z", integrityValid: true },
  { id: "A-1093", userId: "SUP-001", role: "SUPERVISOR", action: "POST /cases/123/dispatch", targetCase: "CASE-123", timestamp: "2026-09-01T10:45:11Z", integrityValid: true },
];

export default function AuditExplorer() {
  const [filterCase, setFilterCase] = useState("");
  const [filterUser, setFilterUser] = useState("");

  const filteredLogs = MOCK_LOGS.filter(log => 
    (filterCase === "" || log.targetCase.includes(filterCase)) &&
    (filterUser === "" || log.userId.includes(filterUser))
  );

  return (
    <div className="p-6 bg-slate-900 min-h-screen">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
          <svg className="w-6 h-6 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" /></svg>
          Audit Log Explorer
        </h1>

        {/* Filters */}
        <div className="flex gap-4 mb-6 p-4 bg-slate-800 rounded-lg border border-slate-700">
          <div>
            <label className="block text-xs text-slate-400 mb-1">Filter by Case</label>
            <input 
              type="text" 
              value={filterCase}
              onChange={(e) => setFilterCase(e.target.value)}
              placeholder="e.g. CASE-123"
              className="p-2 text-sm rounded bg-slate-900 border border-slate-600 text-white outline-none focus:border-indigo-500"
            />
          </div>
          <div>
            <label className="block text-xs text-slate-400 mb-1">Filter by User</label>
            <input 
              type="text" 
              value={filterUser}
              onChange={(e) => setFilterUser(e.target.value)}
              placeholder="e.g. IO-10492"
              className="p-2 text-sm rounded bg-slate-900 border border-slate-600 text-white outline-none focus:border-indigo-500"
            />
          </div>
        </div>

        {/* Table */}
        <div className="bg-slate-800 rounded-lg border border-slate-700 overflow-hidden">
          <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-slate-900 text-slate-400 text-xs uppercase">
              <tr>
                <th className="px-6 py-3 font-medium">Log ID</th>
                <th className="px-6 py-3 font-medium">Timestamp (UTC)</th>
                <th className="px-6 py-3 font-medium">User / Role</th>
                <th className="px-6 py-3 font-medium">Action</th>
                <th className="px-6 py-3 font-medium">Case</th>
                <th className="px-6 py-3 font-medium text-center">Integrity</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-700">
              {filteredLogs.map(log => (
                <tr key={log.id} className="hover:bg-slate-800/50 transition">
                  <td className="px-6 py-4 font-mono text-indigo-300">{log.id}</td>
                  <td className="px-6 py-4 text-slate-400">{log.timestamp}</td>
                  <td className="px-6 py-4">
                    <div className="font-medium text-white">{log.userId}</div>
                    <div className="text-xs text-slate-500">{log.role}</div>
                  </td>
                  <td className="px-6 py-4 font-mono text-xs bg-slate-900 rounded p-1 inline-block mt-2 border border-slate-700">{log.action}</td>
                  <td className="px-6 py-4 text-amber-200">{log.targetCase}</td>
                  <td className="px-6 py-4 text-center">
                    {log.integrityValid ? (
                      <span className="inline-flex items-center gap-1 text-green-400 px-2 py-1 rounded bg-green-900/20 border border-green-500/20">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                        Verified
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1 text-red-400 px-2 py-1 rounded bg-red-900/20 border border-red-500/20">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
                        Corrupt
                      </span>
                    )}
                  </td>
                </tr>
              ))}
              {filteredLogs.length === 0 && (
                <tr>
                  <td colSpan={6} className="px-6 py-8 text-center text-slate-500">
                    No matching audit records found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
