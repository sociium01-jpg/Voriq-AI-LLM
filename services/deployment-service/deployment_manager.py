from typing import Dict, Any, List, Optional

class DeploymentStage(str):
    STAGING = "staging"
    CANARY = "canary"
    PRODUCTION = "production"
    ROLLBACK = "rollback"

class ModelDeploymentManager:
    """Phase 2 Model Registry, Canary Traffic Allocation, and Rollback Manager"""

    def __init__(self):
        self.deployments: Dict[str, Dict[str, Any]] = {}

    def deploy_canary(self, model_id: str, adapter_id: str, traffic_percentage: float = 10.0) -> Dict[str, Any]:
        dep_id = f"dep_{model_id}_canary"
        deployment = {
            "deployment_id": dep_id,
            "model_id": model_id,
            "adapter_ids": [adapter_id],
            "stage": DeploymentStage.CANARY,
            "traffic_percentage": traffic_percentage,
            "fallback_model": "meta-llama/Llama-3.3-70B-Instruct",
            "status": "active",
            "health_check": "healthy"
        }
        self.deployments[dep_id] = deployment
        return deployment

    def rollback(self, deployment_id: str) -> Dict[str, Any]:
        if deployment_id in self.deployments:
            dep = self.deployments[deployment_id]
            dep["stage"] = DeploymentStage.ROLLBACK
            dep["traffic_percentage"] = 0.0
            dep["status"] = "rolled_back"
            return dep
        return {"status": "error", "message": f"Deployment {deployment_id} not found"}
