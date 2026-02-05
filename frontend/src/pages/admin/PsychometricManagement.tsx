import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Brain, Users, Settings, TrendingUp, AlertCircle, Loader2 } from 'lucide-react';
import { PsychometricConfigDialog } from '@/components/molecules/PsychometricConfigDialog';
import { psychometricApi } from '@/lib/api';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { ScrollArea } from '@/components/ui/scroll-area';

const TRAIT_NAMES: Record<number, string> = {
  1: 'Extraversion',
  2: 'Agreeableness',
  3: 'Conscientiousness',
  4: 'Emotional Stability',
  5: 'Intellect/Imagination',
};

const TRAIT_COLORS: Record<number, string> = {
  1: 'bg-blue-500',
  2: 'bg-green-500',
  3: 'bg-purple-500',
  4: 'bg-orange-500',
  5: 'bg-pink-500',
};

export default function PsychometricManagement() {
  const [loading, setLoading] = useState(true);
  const [config, setConfig] = useState<any>(null);
  const [questions, setQuestions] = useState<any[]>([]);
  const [groupedQuestions, setGroupedQuestions] = useState<Record<string, any[]>>({});
  const [error, setError] = useState('');

  const recruiterId = 1; // Get from auth context

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    setError('');

    // Load current configuration
    const configResponse = await psychometricApi.getCurrentConfig(recruiterId);
    if (configResponse.data?.success) {
      setConfig(configResponse.data.config);
    }

    // Load all questions
    const questionsResponse = await psychometricApi.getAllQuestions();
    if (questionsResponse.data?.success) {
      setQuestions(questionsResponse.data.questions);
      setGroupedQuestions(questionsResponse.data.grouped_by_trait);
    } else if (questionsResponse.data?.total_questions === 0) {
      setError('Questions not loaded yet. Please configure the test to load questions.');
    }

    setLoading(false);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center space-y-4">
          <Loader2 className="h-8 w-8 animate-spin mx-auto" />
          <p className="text-muted-foreground">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight flex items-center gap-2">
            <Brain className="h-8 w-8" />
            Psychometric Assessment
          </h1>
          <p className="text-muted-foreground">
            Manage IPIP Big Five personality assessment configuration
          </p>
        </div>
        <PsychometricConfigDialog recruiterId={recruiterId} onConfigSaved={loadData} />
      </div>

      {error && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Stats Cards */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Questions</CardTitle>
            <Brain className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{questions.length}</div>
            <p className="text-xs text-muted-foreground">IPIP Big Five markers</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Questions</CardTitle>
            <Settings className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{config?.num_questions || 50}</div>
            <p className="text-xs text-muted-foreground">
              {config?.selection_mode === 'random' ? 'Random selection' : 'Manual selection'}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Personality Traits</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">5</div>
            <p className="text-xs text-muted-foreground">Big Five dimensions</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Test Status</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {config?.is_active ? (
                <Badge className="bg-green-500">Active</Badge>
              ) : (
                <Badge variant="secondary">Not Configured</Badge>
              )}
            </div>
            <p className="text-xs text-muted-foreground">Configuration status</p>
          </CardContent>
        </Card>
      </div>

      {/* Current Configuration */}
      {config && (
        <Card>
          <CardHeader>
            <CardTitle>Current Configuration</CardTitle>
            <CardDescription>Active psychometric test settings</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm font-medium">Number of Questions</p>
                <p className="text-2xl font-bold">{config.num_questions}</p>
              </div>
              <div>
                <p className="text-sm font-medium">Selection Mode</p>
                <p className="text-2xl font-bold capitalize">{config.selection_mode}</p>
              </div>
            </div>
            {config.desired_traits && (
              <div>
                <p className="text-sm font-medium mb-2">Desired Personality Traits</p>
                <div className="flex flex-wrap gap-2">
                  {JSON.parse(config.desired_traits).map((traitType: number) => (
                    <Badge key={traitType} className={`${TRAIT_COLORS[traitType]} text-white`}>
                      {TRAIT_NAMES[traitType]}
                    </Badge>
                  ))}
                </div>
              </div>
            )}
            {config.selection_mode === 'manual' && config.selected_question_ids && (
              <div>
                <p className="text-sm font-medium mb-2">Selected Questions</p>
                <p className="text-sm text-muted-foreground">
                  {JSON.parse(config.selected_question_ids).length} questions manually selected
                </p>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Questions Library */}
      {questions.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Question Library</CardTitle>
            <CardDescription>All 50 IPIP Big Five personality questions</CardDescription>
          </CardHeader>
          <CardContent>
            <Tabs defaultValue="all">
              <TabsList className="grid w-full grid-cols-6">
                <TabsTrigger value="all">All ({questions.length})</TabsTrigger>
                {Object.entries(TRAIT_NAMES).map(([type, name]) => {
                  const count = questions.filter(q => q.trait_type === parseInt(type)).length;
                  return (
                    <TabsTrigger key={type} value={type}>
                      {name.split('/')[0]} ({count})
                    </TabsTrigger>
                  );
                })}
              </TabsList>

              <TabsContent value="all">
                <ScrollArea className="h-[400px]">
                  <div className="space-y-2 pr-4">
                    {questions.map((q) => (
                      <div key={q.question_id} className="flex items-start gap-3 p-3 border rounded-lg hover:bg-accent">
                        <Badge className={`${TRAIT_COLORS[q.trait_type]} text-white`}>
                          {q.question_id}
                        </Badge>
                        <div className="flex-1">
                          <p className="text-sm">{q.question}</p>
                          <div className="flex items-center gap-2 mt-1">
                            <Badge variant="outline" className="text-xs">
                              {TRAIT_NAMES[q.trait_type]}
                            </Badge>
                            <Badge variant="outline" className="text-xs">
                              {q.scoring_direction === '+' ? 'Direct' : 'Reverse'} scoring
                            </Badge>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </ScrollArea>
              </TabsContent>

              {Object.entries(groupedQuestions).map(([traitName, traitQuestions]) => {
                const traitType = traitQuestions[0]?.trait_type;
                return (
                  <TabsContent key={traitName} value={String(traitType)}>
                    <ScrollArea className="h-[400px]">
                      <div className="space-y-2 pr-4">
                        <Alert>
                          <AlertDescription>
                            <strong>{traitName}</strong> - Questions measuring this personality dimension
                          </AlertDescription>
                        </Alert>
                        {traitQuestions.map((q) => (
                          <div key={q.question_id} className="flex items-start gap-3 p-3 border rounded-lg hover:bg-accent">
                            <Badge className={`${TRAIT_COLORS[q.trait_type]} text-white`}>
                              {q.question_id}
                            </Badge>
                            <div className="flex-1">
                              <p className="text-sm">{q.question}</p>
                              <Badge variant="outline" className="text-xs mt-1">
                                {q.scoring_direction === '+' ? 'Direct' : 'Reverse'} scoring
                              </Badge>
                            </div>
                          </div>
                        ))}
                      </div>
                    </ScrollArea>
                  </TabsContent>
                );
              })}
            </Tabs>
          </CardContent>
        </Card>
      )}

      {/* Info Card */}
      <Card>
        <CardHeader>
          <CardTitle>About IPIP Big Five</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-sm text-muted-foreground">
            The International Personality Item Pool (IPIP) Big Five Factor Markers is a validated 
            psychometric assessment that measures five major personality dimensions:
          </p>
          <div className="grid gap-3">
            {Object.entries(TRAIT_NAMES).map(([type, name]) => (
              <div key={type} className="flex items-start gap-3">
                <Badge className={`${TRAIT_COLORS[parseInt(type)]} text-white`}>{type}</Badge>
                <div>
                  <p className="font-medium">{name}</p>
                  <p className="text-sm text-muted-foreground">
                    {type === '1' && 'Measures sociability, assertiveness, and energy level'}
                    {type === '2' && 'Measures trust, altruism, and cooperation'}
                    {type === '3' && 'Measures organization, responsibility, and dependability'}
                    {type === '4' && 'Measures emotional resilience and calmness'}
                    {type === '5' && 'Measures curiosity, creativity, and open-mindedness'}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
