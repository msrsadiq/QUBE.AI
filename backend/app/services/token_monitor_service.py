"""
Token Monitor Service
--------------------
Real-time token usage monitoring with WebSocket broadcasting.

Features:
- Real-time token usage updates via WebSocket
- Automatic limit checking and alerts
- Usage trend analysis
- Cost tracking
- Periodic usage reports

This service runs as a background task and broadcasts updates to connected clients.
"""

import asyncio
from typing import Dict, Set, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.llm_config import LLMConfig
from app.schemas.llm_config import TokenUsageResponse


class TokenMonitorService:
    """
    Service for monitoring and broadcasting token usage in real-time.
    
    Manages WebSocket connections and periodic usage checks.
    """
    
    def __init__(self):
        """Initialize token monitor service."""
        self.active_connections: Dict[int, Set] = {}  # project_id -> set of websockets
        self.monitor_task: Optional[asyncio.Task] = None
        self.monitor_interval = 5  # seconds
    
    async def connect(self, websocket, project_id: int):
        """
        Register a new WebSocket connection for a project.
        
        Args:
            websocket: WebSocket connection
            project_id: Project ID to monitor
        """
        await websocket.accept()
        
        if project_id not in self.active_connections:
            self.active_connections[project_id] = set()
        
        self.active_connections[project_id].add(websocket)
        
        # Start monitor task if not already running
        if self.monitor_task is None or self.monitor_task.done():
            self.monitor_task = asyncio.create_task(self._monitor_loop())
    
    def disconnect(self, websocket, project_id: int):
        """
        Remove a WebSocket connection.
        
        Args:
            websocket: WebSocket connection to remove
            project_id: Project ID
        """
        if project_id in self.active_connections:
            self.active_connections[project_id].discard(websocket)
            
            # Clean up empty sets
            if not self.active_connections[project_id]:
                del self.active_connections[project_id]
    
    async def broadcast_usage_update(
        self, 
        project_id: int, 
        usage_data: TokenUsageResponse
    ):
        """
        Broadcast token usage update to all connected clients for a project.
        
        Args:
            project_id: Project ID
            usage_data: Token usage data to broadcast
        """
        if project_id not in self.active_connections:
            return
        
        # Convert to dict for JSON serialization
        message = usage_data.dict()
        
        # Broadcast to all connections for this project
        disconnected = set()
        for websocket in self.active_connections[project_id]:
            try:
                await websocket.send_json(message)
            except Exception:
                disconnected.add(websocket)
        
        # Clean up disconnected websockets
        for websocket in disconnected:
            self.disconnect(websocket, project_id)
    
    async def _monitor_loop(self):
        """
        Background task that periodically checks token usage and broadcasts updates.
        """
        from app.core.database import SessionLocal
        
        while self.active_connections:
            try:
                db = SessionLocal()
                
                # Get all projects that have active connections
                active_project_ids = list(self.active_connections.keys())
                
                # Query token usage for active projects
                configs = db.query(LLMConfig).filter(
                    LLMConfig.project_id.in_(active_project_ids),
                    LLMConfig.is_active == True
                ).all()
                
                # Broadcast updates for each config
                for config in configs:
                    usage_data = self._create_usage_response(config)
                    await self.broadcast_usage_update(config.project_id, usage_data)
                
                db.close()
                
            except Exception as e:
                print(f"Error in token monitor loop: {e}")
            
            # Wait before next check
            await asyncio.sleep(self.monitor_interval)
    
    def _create_usage_response(self, config: LLMConfig) -> TokenUsageResponse:
        """
        Create token usage response from config.
        
        Args:
            config: LLM configuration
            
        Returns:
            Token usage response
        """
        daily_percentage = None
        if config.token_limit_daily > 0:
            daily_percentage = round(
                (config.token_usage_today / config.token_limit_daily) * 100, 
                2
            )
        
        monthly_percentage = None
        if config.token_limit_monthly > 0:
            monthly_percentage = round(
                (config.token_usage_month / config.token_limit_monthly) * 100, 
                2
            )
        
        return TokenUsageResponse(
            config_id=config.id,
            project_id=config.project_id,
            token_usage_today=config.token_usage_today,
            token_usage_month=config.token_usage_month,
            token_limit_daily=config.token_limit_daily,
            token_limit_monthly=config.token_limit_monthly,
            daily_usage_percentage=daily_percentage,
            monthly_usage_percentage=monthly_percentage,
            estimated_cost_today=config.estimate_cost(config.token_usage_today),
            estimated_cost_month=config.estimate_cost(config.token_usage_month),
            timestamp=datetime.now()
        )
    
    async def check_usage_alerts(self, db: Session, config: LLMConfig) -> Optional[Dict]:
        """
        Check if usage is approaching limits and return alert if needed.
        
        Args:
            db: Database session
            config: LLM configuration to check
            
        Returns:
            Alert dictionary if limits are being approached, None otherwise
        """
        alerts = []
        
        # Check daily limit
        if config.token_limit_daily > 0:
            usage_pct = (config.token_usage_today / config.token_limit_daily) * 100
            if usage_pct >= 90:
                alerts.append({
                    "type": "daily_limit",
                    "severity": "critical" if usage_pct >= 95 else "warning",
                    "message": f"Daily token limit {usage_pct:.1f}% used",
                    "usage": config.token_usage_today,
                    "limit": config.token_limit_daily
                })
        
        # Check monthly limit
        if config.token_limit_monthly > 0:
            usage_pct = (config.token_usage_month / config.token_limit_monthly) * 100
            if usage_pct >= 90:
                alerts.append({
                    "type": "monthly_limit",
                    "severity": "critical" if usage_pct >= 95 else "warning",
                    "message": f"Monthly token limit {usage_pct:.1f}% used",
                    "usage": config.token_usage_month,
                    "limit": config.token_limit_monthly
                })
        
        return {"config_id": config.id, "alerts": alerts} if alerts else None


# Global instance
token_monitor = TokenMonitorService()