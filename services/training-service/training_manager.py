import uuid
from typing import Dict, Any, List
from vorik_schemas.models import TrainingConfig

class FineTuningManager:
    """Phase 2 LLM Supervised Fine-Tuning, LoRA, and QLoRA Training Orchestrator"""

    def build_training_job(self, cfg: TrainingConfig) -> Dict[str, Any]:
        job_id = f"job_train_{uuid.uuid4().hex[:8]}"

        accelerate_config = {
            "mixed_precision": "bf16",
            "gradient_accumulation_steps": cfg.gradient_accumulation_steps,
            "learning_rate": cfg.learning_rate,
            "max_seq_length": cfg.max_sequence_length,
            "lora_config": {
                "r": cfg.lora_rank or 16,
                "lora_alpha": cfg.lora_alpha or 32,
                "target_modules": ["q_proj", "v_proj", "k_proj", "o_proj"],
                "bias": "none",
                "task_type": "CAUSAL_LM"
            } if cfg.training_type in ["lora", "qlora"] else None
        }

        return {
            "job_id": job_id,
            "status": "queued",
            "output_adapter_path": f"models/adapters/{cfg.output_name}",
            "checkpoint_interval": "500_steps",
            "hyperparameters": accelerate_config,
            "dataset_id": cfg.dataset_id,
            "base_model": cfg.base_model
        }
