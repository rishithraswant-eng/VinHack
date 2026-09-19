import sys
import json

def check_health():
    # Mock offline connections - as required, do not crash, return degraded
    status = {
        "postgres": "degraded",
        "neo4j": "degraded",
        "redis": "degraded",
        "minio": "degraded",
        "overall": "degraded"
    }
    
    print(json.dumps(status, indent=2))
    
    # Exit code 1 since services are degraded (mock offline state)
    sys.exit(1)

if __name__ == "__main__":
    check_health()
