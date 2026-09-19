-- Enable UUID and Cryptographic extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Grant schema privileges
GRANT ALL PRIVILEGES ON DATABASE phantasm TO phantasm;
