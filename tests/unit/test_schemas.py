import pytest
from vorik_schemas.models import (
    UserRole, LanguageEnum, ScriptEnum, UserCreate, LanguageDetectionResult, ModelRoute, TrainingConfig
)

def test_user_role_enum():
    assert UserRole.SUPER_ADMIN.value == "super_admin"
    assert UserRole.MODEL_ENGINEER.value == "model_engineer"

def test_user_create_validation():
    user = UserCreate(
        email="test@vorik.ai",
        password="securepassword123",
        full_name="Rajesh Kumar",
        preferred_language=LanguageEnum.HINDI
    )
    assert user.email == "test@vorik.ai"
    assert user.preferred_language == LanguageEnum.HINDI

def test_model_route_schema():
    route = ModelRoute(
        task_type="code_mixed_conversation",
        language="malayalam",
        script="latin",
        complexity="medium",
        base_model="meta-llama/Llama-3.3-70B-Instruct",
        adapters=["malayalam-romanised-v1"]
    )
    assert route.base_model == "meta-llama/Llama-3.3-70B-Instruct"
    assert "malayalam-romanised-v1" in route.adapters

def test_training_config_schema():
    cfg = TrainingConfig(
        training_type="qlora",
        base_model="meta-llama/Llama-3.3-70B-Instruct",
        dataset_id="ds-001",
        output_name="vorik-hinglish-adapter",
        lora_rank=32
    )
    assert cfg.training_type == "qlora"
    assert cfg.lora_rank == 32
