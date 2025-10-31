-- Create LLM Config table
CREATE TABLE IF NOT EXISTS llm_configs (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    config_name VARCHAR(255) NOT NULL,
    provider VARCHAR(50) NOT NULL,
    model_name VARCHAR(255) NOT NULL,
    api_base_url VARCHAR(500),
    api_key VARCHAR(500),
    temperature VARCHAR(10) DEFAULT '0.7',
    max_tokens INTEGER DEFAULT 2048,
    top_p VARCHAR(10) DEFAULT '1.0',
    provider_specific_params JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT TRUE,
    is_validated BOOLEAN DEFAULT FALSE,
    validation_status VARCHAR(50) DEFAULT 'pending',
    validation_message TEXT,
    last_validated_at TIMESTAMP,
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for llm_configs
CREATE INDEX IF NOT EXISTS idx_llm_configs_project_id ON llm_configs(project_id);
CREATE INDEX IF NOT EXISTS idx_llm_configs_provider ON llm_configs(provider);

-- Create Agent-LLM Mapping table
CREATE TABLE IF NOT EXISTS agent_llm_mappings (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    agent_type VARCHAR(50) NOT NULL,
    llm_config_id INTEGER NOT NULL REFERENCES llm_configs(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for agent_llm_mappings
CREATE INDEX IF NOT EXISTS idx_agent_llm_mappings_project_id ON agent_llm_mappings(project_id);
CREATE INDEX IF NOT EXISTS idx_agent_llm_mappings_agent_type ON agent_llm_mappings(agent_type);
CREATE INDEX IF NOT EXISTS idx_agent_llm_mappings_llm_config_id ON agent_llm_mappings(llm_config_id);
```

---

## Updated Folder Structure (ACTUAL)
```
qube-ai/
│
├── 📁 backend/
│   ├── 📁 app/
│   │   ├── 📁 api/
│   │   │   ├── auth.py
│   │   │   ├── projects.py
│   │   │   └── 📁 routes/
│   │   │       └── llm_config.py ✅
│   │   │
│   │   ├── 📁 core/
│   │   │   ├── config.py
│   │   │   ├── database.py ✅ (KEPT HERE)
│   │   │   ├── dependencies.py ✅ (CORRECTED)
│   │   │   └── security.py
│   │   │
│   │   ├── 📁 models/
│   │   │   ├── user.py
│   │   │   ├── project.py ✅
│   │   │   └── llm_config.py ✅
│   │   │
│   │   ├── 📁 schemas/
│   │   │   ├── auth.py
│   │   │   ├── project.py
│   │   │   └── llm_config.py ✅
│   │   │
│   │   ├── 📁 services/
│   │   │   └── llm_config_service.py ✅
│   │   │
│   │   └── main.py ✅ (CORRECTED)
│   │
│   ├── 📁 venv/
│   ├── .env
│   ├── requirements.txt
│   └── README.md
│
├── 📁 database/
│   ├── 📁 migrations/
│   │   └── 001_create_llm_config_tables.sql ✅ (KEPT HERE)
│   └── ...
│
├── 📁 frontend/
│   ├── 📁 src/
│   │   ├── 📁 app/
│   │   │   ├── 📁 projects/
│   │   │   │   ├── 📁 new/
│   │   │   │   │   └── page.tsx
│   │   │   │   └── 📁 [id]/
│   │   │   │       ├── page.tsx ✅
│   │   │   │       ├── 📁 settings/
│   │   │   │       │   └── page.tsx ✅
│   │   │   │       └── 📁 agents/
│   │   │   │           └── 📁 requirement-analysis/
│   │   │   │               └── page.tsx ✅
│   │   │   └── ...
│   │   │
│   │   └── 📁 components/
│   │       ├── 📁 layout/
│   │       │   ├── Sidebar.tsx ✅ (CORRECT LOCATION)
│   │       │   └── TopBar.tsx
│   │       └── 📁 agents/
│   │           └── UnderDevelopmentAgent.tsx ✅
│   │
│   ├── .env.local
│   ├── package.json
│   └── ...
│
└── README.md