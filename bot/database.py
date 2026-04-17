"""
Gerenciamento de persistência dos alertas em SQLite.
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func

DATABASE_URL = "sqlite:///./alerts.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    symbol = Column(String, nullable=False)
    direction = Column(String, nullable=False)  # 'above' ou 'below'
    target_price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    triggered_at = Column(DateTime(timezone=True), nullable=True)


def init_db():
    """Cria as tabelas no banco."""
    Base.metadata.create_all(bind=engine)


def add_alert(user_id: int, symbol: str, direction: str, target_price: float) -> Alert:
    """Cria um novo alerta."""
    with SessionLocal() as db:
        alert = Alert(
            user_id=user_id,
            symbol=symbol.upper(),
            direction=direction.lower(),
            target_price=target_price,
        )
        db.add(alert)
        db.commit()
        db.refresh(alert)
        return alert


def list_user_alerts(user_id: int):
    """Lista alertas ativos de um usuário."""
    with SessionLocal() as db:
        return (
            db.query(Alert)
            .filter(Alert.user_id == user_id, Alert.is_active == True)
            .all()
        )


def list_all_active_alerts():
    """Lista todos os alertas ativos (usado pelo monitor)."""
    with SessionLocal() as db:
        return db.query(Alert).filter(Alert.is_active == True).all()


def deactivate_alert(alert_id: int, user_id: int) -> bool:
    """Desativa um alerta (só se pertencer ao usuário)."""
    with SessionLocal() as db:
        alert = (
            db.query(Alert)
            .filter(Alert.id == alert_id, Alert.user_id == user_id)
            .first()
        )
        if not alert:
            return False
        alert.is_active = False
        db.commit()
        return True


def trigger_alert(alert_id: int):
    """Marca alerta como disparado."""
    with SessionLocal() as db:
        alert = db.query(Alert).filter(Alert.id == alert_id).first()
        if alert:
            alert.is_active = False
            alert.triggered_at = func.now()
            db.commit()
