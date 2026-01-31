import { Link } from 'react-router-dom';
import { Search, Filter, MoreHorizontal } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { StatusBadge } from '@/components/atoms/StatusBadge';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';

const mockCandidates = [
  {
    id: '1',
    name: 'Sarah Chen',
    email: 'sarah.chen@email.com',
    role: 'Senior Frontend Engineer',
    status: 'completed' as const,
    score: 85,
    date: '2024-01-15',
  },
  {
    id: '2',
    name: 'Marcus Johnson',
    email: 'marcus.j@email.com',
    role: 'Full Stack Developer',
    status: 'in-progress' as const,
    score: null,
    date: '2024-01-16',
  },
  {
    id: '3',
    name: 'Emily Rodriguez',
    email: 'emily.r@email.com',
    role: 'Backend Engineer',
    status: 'pending' as const,
    score: null,
    date: '2024-01-16',
  },
];

export default function Candidates() {
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
        <Button>Add Candidate</Button>
      </div>

      {/* Filters */}
      <Card className="p-4">
        <div className="flex items-center gap-4">
          <div className="relative flex-1 max-w-sm">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input placeholder="Search candidates..." className="pl-9" />
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
              <TableHead>Name</TableHead>
              <TableHead>Role</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Score</TableHead>
              <TableHead>Date</TableHead>
              <TableHead className="w-10"></TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {mockCandidates.map((candidate) => (
              <TableRow key={candidate.id}>
                <TableCell>
                  <Link
                    to={`/admin/candidate/${candidate.id}`}
                    className="hover:underline"
                  >
                    <div>
                      <p className="font-medium">{candidate.name}</p>
                      <p className="text-sm text-muted-foreground">
                        {candidate.email}
                      </p>
                    </div>
                  </Link>
                </TableCell>
                <TableCell>{candidate.role}</TableCell>
                <TableCell>
                  <StatusBadge status={candidate.status} />
                </TableCell>
                <TableCell>
                  {candidate.score !== null ? (
                    <span className="font-medium">{candidate.score}%</span>
                  ) : (
                    <span className="text-muted-foreground">—</span>
                  )}
                </TableCell>
                <TableCell className="text-muted-foreground">
                  {candidate.date}
                </TableCell>
                <TableCell>
                  <Button variant="ghost" size="icon">
                    <MoreHorizontal className="h-4 w-4" />
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Card>
    </div>
  );
}
