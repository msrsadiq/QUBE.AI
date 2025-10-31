'use client';

import { useParams } from 'next/navigation';
import UnderDevelopmentAgent from '@/components/agents/UnderDevelopmentAgent';

export default function RequirementAnalysisAgentPage() {
  const params = useParams();
  const projectId = params.id as string;

  return (
    <UnderDevelopmentAgent
      projectId={projectId}
      agentName="Requirement Analyzer"
      agentDescription="Efficiently analyze and refine project requirements with AI assistance, ensuring clarity and completeness for effective test case generation."
    />
  );
}