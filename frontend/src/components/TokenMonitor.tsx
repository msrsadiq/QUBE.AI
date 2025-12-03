/**
 * Token Monitor Component
 * -----------------------
 * Real-time WebSocket-based token usage monitoring.
 * 
 * Features:
 * - WebSocket connection to backend
 * - Live token usage updates
 * - Usage alerts and warnings
 * - Auto-reconnect on disconnect
 * - Visual progress indicators
 */

'use client';

import { useEffect, useState, useRef } from 'react';

interface TokenMonitorProps {
  projectId: number;
}

interface TokenUsage {
  config_id: number;
  project_id: number;
  token_usage_today: number;
  token_usage_month: number;
  token_limit_daily: number;
  token_limit_monthly: number;
  daily_usage_percentage?: number;
  monthly_usage_percentage?: number;
  estimated_cost_today: number;
  estimated_cost_month: number;
  timestamp: string;
}

export default function TokenMonitor({ projectId }: TokenMonitorProps) {
  const [usageData, setUsageData] = useState<Map<number, TokenUsage>>(new Map());
  const [connected, setConnected] = useState(false);
  const [alerts, setAlerts] = useState<string[]>([]);
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  /**
   * Establish WebSocket connection
   */
  const connect = () => {
    // Get auth token from localStorage
    const token = localStorage.getItem('token');
    if (!token) {
      console.error('No auth token found');
      return;
    }

    // WebSocket URL (adjust based on your backend)
    const wsUrl = `ws://localhost:8000/api/llm-configs/project/${projectId}/monitor`;
    
    try {
      const ws = new WebSocket(wsUrl);
      wsRef.current = ws;

      ws.onopen = () => {
        console.log('WebSocket connected');
        setConnected(true);
        
        // Send ping every 30 seconds to keep connection alive
        const pingInterval = setInterval(() => {
          if (ws.readyState === WebSocket.OPEN) {
            ws.send('ping');
          }
        }, 30000);

        ws.addEventListener('close', () => {
          clearInterval(pingInterval);
        });
      };

      ws.onmessage = (event) => {
        try {
          const data: TokenUsage = JSON.parse(event.data);
          
          // Update usage data
          setUsageData((prev) => {
            const updated = new Map(prev);
            updated.set(data.config_id, data);
            return updated;
          });

          // Check for alerts
          checkForAlerts(data);
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error);
        }
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        setConnected(false);
      };

      ws.onclose = () => {
        console.log('WebSocket disconnected');
        setConnected(false);
        
        // Attempt to reconnect after 5 seconds
        reconnectTimeoutRef.current = setTimeout(() => {
          console.log('Attempting to reconnect...');
          connect();
        }, 5000);
      };
    } catch (error) {
      console.error('Failed to create WebSocket:', error);
      setConnected(false);
    }
  };

  /**
   * Check for usage alerts
   */
  const checkForAlerts = (data: TokenUsage) => {
    const newAlerts: string[] = [];

    if (data.daily_usage_percentage && data.daily_usage_percentage >= 90) {
      newAlerts.push(
        `Config ${data.config_id}: Daily limit ${data.daily_usage_percentage.toFixed(1)}% used`
      );
    }

    if (data.monthly_usage_percentage && data.monthly_usage_percentage >= 90) {
      newAlerts.push(
        `Config ${data.config_id}: Monthly limit ${data.monthly_usage_percentage.toFixed(1)}% used`
      );
    }

    if (newAlerts.length > 0) {
      setAlerts(newAlerts);
      
      // Clear alerts after 10 seconds
      setTimeout(() => setAlerts([]), 10000);
    }
  };

  /**
   * Initialize WebSocket on mount
   */
  useEffect(() => {
    connect();

    // Cleanup on unmount
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
    };
  }, [projectId]);

  /**
   * Get usage color based on percentage
   */
  const getUsageColor = (percentage?: number) => {
    if (!percentage) return 'bg-gray-300';
    if (percentage >= 90) return 'bg-red-500';
    if (percentage >= 70) return 'bg-yellow-500';
    return 'bg-green-500';
  };

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-4">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Live Token Monitoring</h3>
        <div className="flex items-center gap-2">
          <div className={`w-3 h-3 rounded-full ${connected ? 'bg-green-500' : 'bg-red-500'}`} />
          <span className="text-sm text-gray-600">
            {connected ? 'Connected' : 'Disconnected'}
          </span>
        </div>
      </div>

      {/* Alerts */}
      {alerts.length > 0 && (
        <div className="mb-4 space-y-2">
          {alerts.map((alert, index) => (
            <div key={index} className="p-3 bg-yellow-50 border border-yellow-200 rounded-lg text-sm text-yellow-800">
              ⚠️ {alert}
            </div>
          ))}
        </div>
      )}

      {/* Usage Data */}
      {usageData.size === 0 ? (
        <div className="text-center text-gray-500 py-8">
          Waiting for token usage data...
        </div>
      ) : (
        <div className="space-y-4">
          {Array.from(usageData.values()).map((data) => (
            <div key={data.config_id} className="p-4 bg-gray-50 rounded-lg">
              <div className="text-sm font-medium text-gray-700 mb-2">
                Config ID: {data.config_id}
              </div>

              {/* Daily Usage */}
              {data.token_limit_daily > 0 && (
                <div className="mb-3">
                  <div className="flex justify-between text-xs text-gray-600 mb-1">
                    <span>Daily Usage</span>
                    <span>
                      {data.token_usage_today.toLocaleString()} / {data.token_limit_daily.toLocaleString()}
                      {data.daily_usage_percentage && ` (${data.daily_usage_percentage.toFixed(1)}%)`}
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full transition-all duration-300 ${getUsageColor(data.daily_usage_percentage)}`}
                      style={{ width: `${Math.min(data.daily_usage_percentage || 0, 100)}%` }}
                    />
                  </div>
                </div>
              )}

              {/* Monthly Usage */}
              {data.token_limit_monthly > 0 && (
                <div className="mb-2">
                  <div className="flex justify-between text-xs text-gray-600 mb-1">
                    <span>Monthly Usage</span>
                    <span>
                      {data.token_usage_month.toLocaleString()} / {data.token_limit_monthly.toLocaleString()}
                      {data.monthly_usage_percentage && ` (${data.monthly_usage_percentage.toFixed(1)}%)`}
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full transition-all duration-300 ${getUsageColor(data.monthly_usage_percentage)}`}
                      style={{ width: `${Math.min(data.monthly_usage_percentage || 0, 100)}%` }}
                    />
                  </div>
                </div>
              )}

              {/* Cost */}
              <div className="flex justify-between text-xs text-gray-600 mt-2">
                <span>Est. Cost (Month):</span>
                <span className="font-medium">${data.estimated_cost_month.toFixed(4)}</span>
              </div>

              <div className="text-xs text-gray-400 mt-1">
                Last update: {new Date(data.timestamp).toLocaleTimeString()}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}