/**
 * Agent Card Component
 * --------------------
 * Card representing an AI agent module on the project dashboard.
 * 
 * Features:
 * - Icon and name display
 * - Description of agent capabilities
 * - Hover effect with scale animation
 * - Click-through navigation to agent page
 * 
 * Props:
 * - agent: Agent data (id, name, icon, description, route)
 * - onClick: Callback when card is clicked
 * 
 * Agent Types:
 * QE Agents:
 *   - Requirement Analyzer
 *   - Testcase Generator
 *   - Bugs Manager
 * 
 * Automation Agents:
 *   - Page Object Generator
 *   - Framework Agent
 *   - API Agent
 * 
 * Design:
 * - Teal border (#17A2B8)
 * - Large emoji icon
 * - Hover scale effect (105%)
 * - Shadow elevation on hover
 */

'use client';

interface Agent {
  /** Unique agent identifier (kebab-case) */
  id: string;
  /** Display name of the agent */
  name: string;
  /** Emoji icon representing the agent */
  icon: string;
  /** Description of agent capabilities */
  description: string;
  /** Navigation route to agent page */
  route: string;
}

interface AgentCardProps {
  /** Agent data to display */
  agent: Agent;
  /** Callback when card is clicked */
  onClick: () => void;
}

export default function AgentCard({ agent, onClick }: AgentCardProps) {
  return (
    <div
      onClick={onClick}
      className="bg-white border-2 border-primary-500 rounded-lg p-6 cursor-pointer hover:shadow-lg transition-all hover:scale-105"
      role="button"
      tabIndex={0}
      onKeyPress={(e) => e.key === 'Enter' && onClick()}
      aria-label={`Open ${agent.name}`}
    >
      {/* AGENT HEADER - Icon and Name */}
      <div className="flex items-start gap-4 mb-4">
        {/* Agent Icon (Emoji) */}
        <div className="text-4xl" aria-hidden="true">
          {agent.icon}
        </div>
        
        {/* Agent Name */}
        <div className="flex-1">
          <h3 className="text-xl font-bold text-gray-800 mb-2">
            {agent.name}
          </h3>
        </div>
      </div>
      
      {/* AGENT DESCRIPTION */}
      <p className="text-gray-600 text-sm leading-relaxed">
        {agent.description}
      </p>
    </div>
  );
}