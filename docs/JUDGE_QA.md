# PHANTASM: Judge Q&A Cue Cards

### Q: "Why not just use Chainalysis or TRM Labs?"
PHANTASM is cheaper for local cyber cells, avoids per-seat licensing fees, and integrates natively with India's SAHYOG portal. Instead of just relying on static databases, it actively models unseen mule wallets using structural and temporal graphs. It is a complement to these tools, not a replacement.

### Q: "How do you handle mixing services like Tornado Cash or cross-chain bridges like Stargate?"
We identify mixer smart contracts at the bytecode level and perform temporal correlation on withdrawals across candidate VASPs. Bridges are tracked using our chain-sharded graph's bridge-index layer, allowing cross-chain hops. Full tracing isn't guaranteed, but the confidence score honestly reflects any uncertainty.

### Q: "What if the attribution is wrong?"
Our output isn't a binary verdict; it includes a Monte Carlo-derived confidence score. If the score is low, it requires mandatory human review. Furthermore, our Merkle-proof-backed evidence trail allows any party to independently verify the transactions, ensuring accountability.

### Q: "How does this scale beyond a hackathon demo to national case volume?"
Our system uses a chain-sharded graph database and separate worker pools per blockchain for horizontal scaling. We also use Redis for live edge caching, so repeated queries are served from memory. Scaling up simply means adding more shards and workers to existing government cloud infrastructure.

### Q: "Is the Elliptic dataset enough to train a production-grade classifier?"
No, it's only a starting point for prototyping and benchmarking. A production deployment requires FIU-IND-provided case data to fine-tune the model specifically on Indian laundering typologies. We have designed the fine-tuning pipeline into the architecture from the beginning for this exact purpose.

### Q: "What is the actual latency per wallet trace?"
We are benchmarking the prototype, but the main limits are API rate constraints from public block explorers. We mitigate this using caching and multi-source ingestion. The graph query time and Monte Carlo simulations also add latency, which we balance against accuracy.
