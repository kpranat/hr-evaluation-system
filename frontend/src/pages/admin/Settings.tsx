import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { Separator } from '@/components/ui/separator';
import { useState } from 'react';
import MCQUploadDialog from '@/components/molecules/MCQUploadDialog';
import TextBasedUploadDialog from '@/components/molecules/TextBasedUploadDialog';
import { Upload } from 'lucide-react';

export default function Settings() {
  const [mcqDialogOpen, setMcqDialogOpen] = useState(false);
  const [textBasedDialogOpen, setTextBasedDialogOpen] = useState(false);

  return (
    <div className="space-y-6 animate-fade-in max-w-2xl">
      {/* Page Header */}
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Settings</h1>
        <p className="text-muted-foreground">
          Configure your HR evaluation system preferences.
        </p>
      </div>

      {/* General Settings */}
      <Card className="p-6 space-y-6">
        <div>
          <h2 className="text-lg font-semibold">General</h2>
          <p className="text-sm text-muted-foreground">
            Basic configuration for your organization.
          </p>
        </div>

        <Separator />

        <div className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="company">Company Name</Label>
            <Input id="company" placeholder="Your Company" />
          </div>

          <div className="space-y-2">
            <Label htmlFor="email">Notification Email</Label>
            <Input id="email" type="email" placeholder="hr@company.com" />
          </div>
        </div>
      </Card>

      {/* MCQ Management */}
      <Card className="p-6 space-y-6">
        <div>
          <h2 className="text-lg font-semibold">MCQ Question Bank</h2>
          <p className="text-sm text-muted-foreground">
            Upload and manage multiple choice questions for assessments.
          </p>
        </div>

        <Separator />

        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="space-y-0.5">
              <Label>Bulk Upload Questions</Label>
              <p className="text-sm text-muted-foreground">
                Upload MCQ questions from CSV or Excel file
              </p>
            </div>
            <Button onClick={() => setMcqDialogOpen(true)}>
              <Upload className="mr-2 h-4 w-4" />
              Upload MCQs
            </Button>
          </div>
        </div>
      </Card>

      {/* Text-Based Question Management */}
      <Card className="p-6 space-y-6">
        <div>
          <h2 className="text-lg font-semibold">Text-Based Question Bank</h2>
          <p className="text-sm text-muted-foreground">
            Upload and manage open-ended questions for text-based assessments.
          </p>
        </div>

        <Separator />

        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="space-y-0.5">
              <Label>Bulk Upload Questions</Label>
              <p className="text-sm text-muted-foreground">
                Upload text-based questions from CSV or Excel file (max 200 words per answer)
              </p>
            </div>
            <Button onClick={() => setTextBasedDialogOpen(true)}>
              <Upload className="mr-2 h-4 w-4" />
              Upload Questions
            </Button>
          </div>
        </div>
      </Card>

      {/* Assessment Settings */}
      <Card className="p-6 space-y-6">
        <div>
          <h2 className="text-lg font-semibold">Assessment</h2>
          <p className="text-sm text-muted-foreground">
            Configure how assessments are delivered and scored.
          </p>
        </div>

        <Separator />

        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="space-y-0.5">
              <Label>Enable Proctoring</Label>
              <p className="text-sm text-muted-foreground">
                Monitor candidates during assessments
              </p>
            </div>
            <Switch defaultChecked />
          </div>

          <div className="flex items-center justify-between">
            <div className="space-y-0.5">
              <Label>AI-Generated Questions</Label>
              <p className="text-sm text-muted-foreground">
                Generate personalized questions based on resume
              </p>
            </div>
            <Switch defaultChecked />
          </div>

          <div className="flex items-center justify-between">
            <div className="space-y-0.5">
              <Label>Auto-Advance Questions</Label>
              <p className="text-sm text-muted-foreground">
                Automatically move to next question after time limit
              </p>
            </div>
            <Switch />
          </div>
        </div>
      </Card>

      {/* API Settings */}
      <Card className="p-6 space-y-6">
        <div>
          <h2 className="text-lg font-semibold">API Configuration</h2>
          <p className="text-sm text-muted-foreground">
            Backend integration settings.

      {/* Text-Based Upload Dialog */}
      <TextBasedUploadDialog
        open={textBasedDialogOpen}
        onOpenChange={setTextBasedDialogOpen}
        onUploadComplete={() => {
          console.log('Text-based questions upload completed');
        }}
      />
          </p>
        </div>

        <Separator />

        <div className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="api-url">Flask API URL</Label>
            <Input
              id="api-url"
              placeholder="http://localhost:5000"
              defaultValue="http://localhost:5000"
            />
          </div>
        </div>

        <Button>Save Changes</Button>
      </Card>

      {/* MCQ Upload Dialog */}
      <MCQUploadDialog
        open={mcqDialogOpen}
        onOpenChange={setMcqDialogOpen}
        onUploadComplete={() => {
          console.log('MCQ upload completed');
        }}
      />
    </div>
  );
}
