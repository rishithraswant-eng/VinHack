import os

def replace_in_file(path, old, new):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if old in content:
        content = content.replace(old, new)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {path}")
    else:
        print(f"Could not find target in {path}")

replace_in_file('backend/app/audit/verifier.py', 
    'if start_id is not None and len(logs) > 0:\n            if logs[0].prev_entry_hash:\n                expected_prev_hash = logs[0].prev_entry_hash',
    'if start_id is not None and len(logs) > 0 and logs[0].prev_entry_hash:\n            expected_prev_hash = logs[0].prev_entry_hash')

replace_in_file('backend/app/core/audit_middleware.py',
    'except Exception:\n                pass',
    'except Exception as e:\n                import logging\n                logging.debug(f"Token error: {e}")')

replace_in_file('backend/app/core/ratelimit.py',
    'raise e',
    'raise')

replace_in_file('backend/app/core/security.py',
    'def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)):',
    'def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)):  # noqa: B008')

replace_in_file('backend/app/core/security.py',
    'def role_checker(user: dict = Depends(get_current_user)):',
    'def role_checker(user: dict = Depends(get_current_user)):  # noqa: B008')

replace_in_file('backend/app/graph/neo4j_client.py',
    'from neo4j import AsyncGraphDatabase, AsyncSession',
    'from neo4j import AsyncGraphDatabase')

replace_in_file('backend/app/ml/graph_dataset.py',
    'def __init__(self, dataset_path: str = None):',
    'def __init__(self, dataset_path: str | None = None):')

replace_in_file('backend/app/ml/graph_dataset.py',
    'raw_labels = [1, 2, 3, 2, 1]',
    '# raw_labels = [1, 2, 3, 2, 1]')

replace_in_file('backend/app/ml/models/tgn.py',
    'z, last_update = self.memory(n_id)',
    'z, _last_update = self.memory(n_id)')

replace_in_file('backend/app/ml/trainer.py',
    'y_pred = [0, 1] if len(y_true) >= 2 else [0]*len(y_true)',
    '# y_pred')

replace_in_file('backend/app/ml/trainer.py',
    'y_pred = [1, 0] if len(y_true) >= 2 else [0]*len(y_true)',
    '# y_pred')

replace_in_file('backend/app/models/canonical.py',
    '__table_args__ = (',
    'from typing import ClassVar\n    __table_args__: ClassVar = (')

replace_in_file('backend/app/tpp/hawkes.py',
    'def __init__(self, mu: float = None, alpha: float = None, beta: float = None):',
    'def __init__(self, mu: float | None = None, alpha: float | None = None, beta: float | None = None):')

replace_in_file('backend/scripts/seed_demo.py',
    'except Exception as e:\n                logging.warning(f"Ignoring duplicate or schema insert error: {e}")',
    'except Exception as e:\n                import logging\n                logger = logging.getLogger(__name__)\n                logger.warning(f"Ignoring duplicate or schema insert error: {e}")')

print("All done.")
