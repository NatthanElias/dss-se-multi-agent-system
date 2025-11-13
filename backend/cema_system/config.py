from dataclasses import dataclass, field
from typing import Literal, Optional
from pathlib import Path


@dataclass
class ModelConfig:    
    # Default model for all agents
    default_model: str = "gemini-2.5-flash"
    
    # Agent-specific models (override default if needed)
    cso_model: Optional[str] = None
    cmo_model: Optional[str] = None
    cfo_model: Optional[str] = None
    cro_model: Optional[str] = None
    ceo_model: Optional[str] = None # "gemini-2.5-pro"
    
    # Generation parameters
    temperature: float = 0.3
    max_tokens: int = 8000
    top_p: float = 0.95
    top_k: int = 40


@dataclass
class LanguageConfig:
    output_language: Literal['pt-BR', 'en-US', 'es-ES'] = 'pt-BR'
    
    # Language names for prompts
    language_names = {
        'pt-BR': 'Portuguese (Brazil)',
        'en-US': 'English (US)',
        'es-ES': 'Spanish (Spain)'
    }
    
    @property
    def language_instruction(self) -> str:
        """Returns instruction for agents about output language."""
        lang_name = self.language_names[self.output_language]
        return f"\nCRITICAL: You MUST respond in {lang_name}. ALL output must be in {lang_name}."


@dataclass
class KnowledgeBaseConfig:
    """Knowledge base paths and settings."""
    
    # Base path
    base_path: Path = Path(__file__).parent.parent / "knowledge_base"
    
    # Organization size: 'PEQUENA', 'MEDIA', 'GRANDE'
    org_size: Literal['PEQUENA', 'MEDIA', 'GRANDE'] = 'PEQUENA'
    
    # Document filenames (can override if different naming)
    doc1_mission: str = "doc1_mission_vision_values.md"
    doc2_dre: str = "doc2_dre.csv"
    doc3_social: str = "doc3_social_impact_report.md"
    doc4_canvas: str = "doc4_business_model_canvas.md"
    doc5_swot: str = "doc5_swot_analysis.md"
    
    @property
    def kb_path(self) -> Path:
        return self.base_path / self.org_size


@dataclass
class AgentConfig:
    # Enable/disable specific agents (for testing)
    enable_cso: bool = True
    enable_cmo: bool = True
    enable_cfo: bool = True
    enable_cro: bool = True
    enable_ceo: bool = True
    
    # Timeout per agent (seconds)
    timeout: int = 120
    
    # Retry configuration
    max_retries: int = 3
    retry_delay: float = 2.0  # seconds


@dataclass
class SystemConfig:
    """System-wide configuration."""
    
    # Logging
    log_level: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR'] = 'INFO'
    log_to_file: bool = True
    log_file_path: Path = Path("/tmp/cema_system.log")
    
    parallel_execution: bool = True  # False = sequential for debugging
    
    # Output formatting
    use_markdown: bool = True
    include_timestamps: bool = True


@dataclass
class CEMAConfig:
    """Complete CEMA system configuration."""
    
    model: ModelConfig = field(default_factory=ModelConfig)
    language: LanguageConfig = field(default_factory=LanguageConfig)
    knowledge_base: KnowledgeBaseConfig = field(default_factory=KnowledgeBaseConfig)
    agents: AgentConfig = field(default_factory=AgentConfig)
    system: SystemConfig = field(default_factory=SystemConfig)


# GLOBAL CONFIG INSTANCE
config = CEMAConfig()


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_model_for_agent(agent_name: str) -> str:
    """
    Get the appropriate model for a specific agent.
    
    Args:
        agent_name: Name of the agent ('cso', 'cmo', 'cfo', 'cro', 'ceo')
        
    Returns:
        str: Model ID to use
    """
    agent_model = getattr(config.model, f"{agent_name}_model")
    return agent_model if agent_model else config.model.default_model


def update_config_from_env():
    """
    Override config values from environment variables.
    Useful for Docker/production deployments.
    """
    import os
    
    # Model configuration
    if model := os.getenv('CEMA_MODEL'):
        config.model.default_model = model
    
    if temp := os.getenv('CEMA_TEMPERATURE'):
        config.model.temperature = float(temp)
    
    # Language configuration
    if lang := os.getenv('CEMA_LANGUAGE'):
        if lang in ['pt-BR', 'en-US', 'es-ES']:
            config.language.output_language = lang
    
    # Knowledge base
    if org_size := os.getenv('CEMA_ORG_SIZE'):
        if org_size in ['PEQUENA', 'MEDIA', 'GRANDE']:
            config.knowledge_base.org_size = org_size
    
    # Logging
    if log_level := os.getenv('CEMA_LOG_LEVEL'):
        if log_level in ['DEBUG', 'INFO', 'WARNING', 'ERROR']:
            config.system.log_level = log_level


# Auto-load from environment on import
update_config_from_env()
