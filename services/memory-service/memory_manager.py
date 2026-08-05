from typing import Dict, Any, List, Optional
from vorik_db.connection import SessionLocal
from vorik_db.models import AgentMemoryDB

class MemoryManager:
    """
    Tenant-isolated Memory Manager supporting 8 memory categories:
    Working, Conversation, User Preference, Project, Organisation, 
    Episodic Agent, Tool-Result, and Semantic Retrieval.
    """
    def set_memory(
        self, user_id: str, tenant_id: str, memory_type: str, key: str, value: Any
    ) -> Dict[str, Any]:
        db = SessionLocal()
        try:
            # Check existing memory record for key
            existing = db.query(AgentMemoryDB).filter_by(
                user_id=user_id, tenant_id=tenant_id, memory_type=memory_type, key=key
            ).first()

            if existing:
                existing.value = value
            else:
                memory_rec = AgentMemoryDB(
                    user_id=user_id,
                    tenant_id=tenant_id,
                    memory_type=memory_type,
                    key=key,
                    value=value
                )
                db.add(memory_rec)

            db.commit()
            return {"status": "saved", "key": key, "tenant_id": tenant_id}
        except Exception as e:
            db.rollback()
            return {"status": "error", "message": str(e)}
        finally:
            db.close()

    def get_memory(
        self, user_id: str, tenant_id: str, memory_type: str, key: str
    ) -> Optional[Any]:
        db = SessionLocal()
        try:
            record = db.query(AgentMemoryDB).filter_by(
                user_id=user_id, tenant_id=tenant_id, memory_type=memory_type, key=key
            ).first()
            return record.value if record else None
        finally:
            db.close()

    def delete_memory(
        self, user_id: str, tenant_id: str, memory_type: str, key: str
    ) -> bool:
        db = SessionLocal()
        try:
            record = db.query(AgentMemoryDB).filter_by(
                user_id=user_id, tenant_id=tenant_id, memory_type=memory_type, key=key
            ).first()
            if record:
                db.delete(record)
                db.commit()
                return True
            return False
        except Exception:
            db.rollback()
            return False
        finally:
            db.close()

    def list_user_memories(self, user_id: str, tenant_id: str) -> List[Dict[str, Any]]:
        db = SessionLocal()
        try:
            records = db.query(AgentMemoryDB).filter_by(user_id=user_id, tenant_id=tenant_id).all()
            return [
                {"id": r.id, "memory_type": r.memory_type, "key": r.key, "value": r.value, "created_at": str(r.created_at)}
                for r in records
            ]
        finally:
            db.close()

memory_manager = MemoryManager()
