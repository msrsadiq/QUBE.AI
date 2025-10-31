'use client';

import { useRouter } from 'next/navigation';
import Sidebar from '@/components/layout/Sidebar';
import TopBar from '@/components/layout/TopBar';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Zap } from 'lucide-react';

interface UnderDevelopmentAgentProps {
  projectId: string;
  agentName: string;
  agentDescription: string;
}

export default function UnderDevelopmentAgent({
  projectId,
  agentName,
  agentDescription,
}: UnderDevelopmentAgentProps) {
  const router = useRouter();

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar projectId={projectId} />

      <div className="flex-1 flex flex-col">
        <TopBar />

        <main className="flex-1 overflow-auto flex items-center justify-center p-8">
          <Card className="w-full max-w-md border-teal-200">
            <CardContent className="pt-12 pb-12 text-center">
              <div className="flex justify-center mb-6">
                <div className="p-4 bg-teal-100 rounded-full">
                  <Zap className="w-12 h-12 text-teal-600" />
                </div>
              </div>

              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                {agentName}
              </h1>

              <p className="text-gray-600 mb-8">
                {agentDescription}
              </p>

              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-8">
                <p className="text-sm text-yellow-800 font-semibold mb-2">
                  🚀 Coming Soon
                </p>
                <p className="text-xs text-yellow-700">
                  This agent is currently under development. Check back soon for exciting features!
                </p>
              </div>

              <Button
                onClick={() => router.push(`/projects/${projectId}`)}
                className="bg-teal-600 hover:bg-teal-700 text-white"
              >
                Back to Project Dashboard
              </Button>
            </CardContent>
          </Card>
        </main>
      </div>
    </div>
  );
}