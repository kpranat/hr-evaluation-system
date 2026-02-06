import { Link } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { Search, Filter, MoreHorizontal, Upload, RotateCcw, Unlock, Eye, AlertCircle } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { StatusBadge } from '@/components/atoms/StatusBadge';
import BulkUploadDialog from '@/components/molecules/BulkUploadDialog';
import { adminApi, recruiterApi } from '@/lib/api';
import { useToast } from '@/hooks/use-toast';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';

interface Candidate {
  id: number;
  email: string;
  name?: string;
  role?: string;
  overall_score: number | null;
  status: 'completed' | 'in-progress' | 'pending';
  applied_date: string;
  suspension_info?: {
    is_suspended: boolean;
    suspension_reason: string;
    resume_allowed: boolean;
  };
}

export default function Candidates() {
  const [uploadDialogOpen, setUploadDialogOpen] = useState(false);
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [resetDialogOpen, setResetDialogOpen] = useState(false);
  const [selectedCandidate, setSelectedCandidate] = useState<Candidate | null>(null);
  const { toast } = useToast();

  const fetchCandidates = async () => {
    setLoading(true);
    const { data, error } = await adminApi.getCandidates();
    
    if (error) {
      toast({
        title: 'Error',
        description: 'Failed to load candidates',
        variant: 'destructive',
      });
    } else if (data?.success && data?.candidates) {
      setCandidates(data.candidates);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchCandidates();
  }, []);

  const handleUploadComplete = () => {
    toast({
      title: 'Success',
      description: 'Candidates uploaded successfully',
    });
    fetchCandidates();
  };

  const handleAllowResume = async (candidate: Candidate) => {
    const { data, error } = await recruiterApi.allowResume(candidate.id);
    
    if (error || !data?.success) {
      toast({
        title: 'Error',
        description: error || 'Failed to authorize resume',
        variant: 'destructive',
      });
    } else {
      toast({
        title: 'Success',
        description: `${candidate.email} can now resume their exam`,
      });
      fetchCandidates();
    }
  };

  const handleResetExam = async () => {
    if (!selectedCandidate) return;
    
    const { data, error } = await recruiterApi.resetExam(selectedCandidate.id);
    
    if (error || !data?.success) {
      toast({
        title: 'Error',
        description: error || 'Failed to reset exam',
        variant: 'destructive',
      });
    } else {
      toast({
        title: 'Success',
        description: data.message || 'Exam reset successfully',
      });
      fetchCandidates();
    }
    setResetDialogOpen(false);
    setSelectedCandidate(null);
  };

  const filteredCandidates = candidates.filter((candidate) =>
    candidate.email.toLowerCase().includes(searchQuery.toLowerCase()) ||
    (candidate.name?.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Candidates</h1>
          <p className="text-muted-foreground">
            Manage and review all candidate assessments.
          </p>
        </div>
        <Button onClick={() => setUploadDialogOpen(true)}>
          <Upload className="mr-2 h-4 w-4" />
          Add Candidates
        </Button>
      </div>

      {/* Filters */}
      <Card className="p-4">
        <div className="flex items-center gap-4">
          <div className="relative flex-1 max-w-sm">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input 
              placeholder="Search candidates..." 
              className="pl-9" 
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
          <Button variant="outline" size="icon">
            <Filter className="h-4 w-4" />
          </Button>
        </div>
      </Card>

      {/* Candidates Table */}
      <Card>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name/Email</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Score</TableHead>
              <TableHead>Date</TableHead>
              <TableHead className="w-10"></TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={5} className="text-center py-8">
                  <div className="flex items-center justify-center gap-2">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary"></div>
                    <span className="text-muted-foreground">Loading candidates...</span>
                  </div>
                </TableCell>
              </TableRow>
            ) : filteredCandidates.length === 0 ? (
              <TableRow>
                <TableCell colSpan={5} className="text-center py-8">
                  <p className="text-muted-foreground">
                    {searchQuery ? 'No candidates found matching your search' : 'No candidates yet. Upload candidates to get started.'}
                  </p>
                </TableCell>
              </TableRow>
            ) : (
              filteredCandidates.map((candidate) => (
                <TableRow key={candidate.id}>
                  <TableCell>
                    <Link
                      to={`/admin/candidate/${candidate.id}`}
                      className="hover:underline"
                    >
                      <div>
                        <p className="font-medium">{candidate.name || candidate.email.split('@')[0]}</p>
                        <p className="text-sm text-muted-foreground">
                          {candidate.email}
                        </p>
                      </div>
                    </Link>
                    {candidate.suspension_info?.is_suspended && (
                      <div className="flex items-center gap-1 mt-1">
                        <AlertCircle className="h-3 w-3 text-amber-500" />
                        <span className="text-xs text-amber-600">
                          Exam suspended - {candidate.suspension_info.suspension_reason}
                        </span>
                      </div>
                    )}
                  </TableCell>
                  <TableCell>
                    <StatusBadge status={candidate.status} />
                  </TableCell>
                  <TableCell>
                    {candidate.overall_score !== null ? (
                      <span className="font-medium">{Math.round(candidate.overall_score)}%</span>
                    ) : (
                      <span className="text-muted-foreground">—</span>
                    )}
                  </TableCell>
                  <TableCell className="text-muted-foreground">
                    {candidate.applied_date !== 'N/A' ? candidate.applied_date : '—'}
                  </TableCell>
                  <TableCell>
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="ghost" size="icon">
                          <MoreHorizontal className="h-4 w-4" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuLabel>Actions</DropdownMenuLabel>
                        <DropdownMenuSeparator />
                        <DropdownMenuItem asChild>
                          <Link to={`/admin/candidate/${candidate.id}`}>
                            <Eye className="mr-2 h-4 w-4" />
                            View Details
                          </Link>
                        </DropdownMenuItem>
                        {candidate.suspension_info?.is_suspended && !candidate.suspension_info.resume_allowed && (
                          <DropdownMenuItem onClick={() => handleAllowResume(candidate)}>
                            <Unlock className="mr-2 h-4 w-4" />
                            Allow Resume
                          </DropdownMenuItem>
                        )}
                        <DropdownMenuItem 
                          onClick={() => {
                            setSelectedCandidate(candidate);
                            setResetDialogOpen(true);
                          }}
                          className="text-destructive focus:text-destructive"
                        >
                          <RotateCcw className="mr-2 h-4 w-4" />
                          Reset Exam
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </Card>

      {/* Bulk Upload Dialog */}
      <BulkUploadDialog
        open={uploadDialogOpen}
        onOpenChange={setUploadDialogOpen}
        onUploadComplete={handleUploadComplete}
      />

      {/* Reset Confirmation Dialog */}
      <AlertDialog open={resetDialogOpen} onOpenChange={setResetDialogOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Reset Exam?</AlertDialogTitle>
            <AlertDialogDescription>
              This will completely reset the exam for <strong>{selectedCandidate?.email}</strong>.
              All progress, answers, and session data will be deleted. The candidate will be able to retake all assessments from scratch.
              <br /><br />
              This action cannot be undone.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction onClick={handleResetExam} className="bg-destructive text-destructive-foreground hover:bg-destructive/90">
              Reset Exam
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
}
