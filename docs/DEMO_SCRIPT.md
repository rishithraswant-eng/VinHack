SCENE 1 — Case Creation (2 min)
  - Open browser: http://localhost:3000
  - Show MOCK chip visible at top
  - Create case with FIR DL-CYBER-2025-001
  - Show authority gate blocks without FIR number

SCENE 2 — Trace Execution (3 min)
  - POST /cases/{id}/trace via UI or curl
  - Show WebSocket progress stages: INGESTING → CLASSIFYING → ATTRIBUTING → SEALING
  - Show attributed VASP: DemoExchange, 3 hops, confidence 0.87

SCENE 3 — Merkle Proof Verification (2 min)
  - Show dossier PDF with proof hashes
  - Run verify_proof() live in Python shell
  - Show tampered hash fails verification

SCENE 4 — SAHYOG Dispatch (1 min)
  - Show pre-filled disclosure request
  - Show [MOCK] label on dispatch result
  - Explain: real connector pending OQ-01 resolution

SCENE 5 — Judge Q&A prep (2 min)
  - Confidence score: explain CI, requires_review flag
  - Limitations section in dossier
  - Why not Chainalysis: SAHYOG integration, Merkle proofs, cost
