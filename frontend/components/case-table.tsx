'use client';
import { useRouter } from 'next/navigation';
import { useState, useEffect } from 'react';
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { ArrowDown, ArrowUp } from 'lucide-react';
import { fetchCases } from '@/lib/api';

type CaseStatus =
    | 'in favour of defendant'
    | 'in favour of plaintiff'
    | 'settled'
    | 'in progress first instance'
    | 'dismissed'
    | 'in progress appeal'
    | 'in progress supreme court';
type SortField =
    | 'title'
    | 'status'
    | 'jurisdiction'
    | 'caseType'
    | 'date'
    | 'brandImpact'
    | 'risk';
type SortDirection = 'asc' | 'desc';

interface CaseTableProps {
    searchQuery: string;
}

export function CaseTable({ searchQuery }: CaseTableProps) {
    const router = useRouter();
    const [sortField, setSortField] = useState<SortField>('date');
    const [sortDirection, setSortDirection] = useState<SortDirection>('desc');
    const [cases, setCases] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function loadCases() {
            setLoading(true);
            const casesData = await fetchCases(searchQuery);
            console.log('Fetched cases:', casesData);
            setCases(casesData);
            setLoading(false);
        }

        loadCases();
    }, [searchQuery]);

    // Sort cases based on sort field and direction
    const sortedCases = [...cases].sort((a, b) => {
        if (sortField === 'status') {
            // Custom sort order for status: "in progress" > "won" > "lost"
            const statusOrder = { 'in progress': 0, won: 1, lost: 2 };
            const aValue = statusOrder[a.status as keyof typeof statusOrder];
            const bValue = statusOrder[b.status as keyof typeof statusOrder];
            return sortDirection === 'asc' ? aValue - bValue : bValue - aValue;
        }

        if (sortField === 'date') {
            const aDate = new Date(a.date).getTime();
            const bDate = new Date(b.date).getTime();
            return sortDirection === 'asc' ? aDate - bDate : bDate - aDate;
        }

        if (sortField === 'brandImpact') {
            const impactOrder = { High: 0, Medium: 1, Low: 2 };
            const aImpact = a.brandImpactEstimate?.impact || 'Low';
            const bImpact = b.brandImpactEstimate?.impact || 'Low';
            const aValue = impactOrder[aImpact as keyof typeof impactOrder];
            const bValue = impactOrder[bImpact as keyof typeof impactOrder];
            return sortDirection === 'asc' ? aValue - bValue : bValue - aValue;
        }

        if (sortField === 'risk') {
            const riskOrder = { High: 0, Medium: 1, Low: 2 };
            const aRisk = a.caseWinLikelihood?.likelihood || 'Low';
            const bRisk = b.caseWinLikelihood?.likelihood || 'Low';
            const aValue = riskOrder[aRisk as keyof typeof riskOrder];
            const bValue = riskOrder[bRisk as keyof typeof riskOrder];
            return sortDirection === 'asc' ? aValue - bValue : bValue - aValue;
        }

        const aValue = a[sortField];
        const bValue = b[sortField];

        if (aValue < bValue) return sortDirection === 'asc' ? -1 : 1;
        if (aValue > bValue) return sortDirection === 'asc' ? 1 : -1;
        return 0;
    });

    const getStatusColor = (status: CaseStatus) => {
        const status_lower = status.toLowerCase();
        if (status_lower.includes('in progress')) {
            return 'bg-blue-500 hover:bg-blue-600';
        }

        switch (status_lower) {
            case 'in favour of defendant':
                return 'bg-green-500 hover:bg-green-600';
            case 'in favour of plaintiff':
                return 'bg-red-500 hover:bg-red-600';
            case 'settled':
                return 'bg-yellow-500 hover:bg-yellow-600';
            case 'dismissed':
                return 'bg-gray-500 hover:bg-gray-600';
            default:
                return 'bg-gray-300 hover:bg-gray-400';
        }
    };

    const getBrandImpactColor = (impact: string) => {
        switch (impact) {
            case 'High':
                return 'bg-red-500 hover:bg-red-600';
            case 'Medium':
                return 'bg-yellow-500 hover:bg-yellow-600';
            case 'Low':
                return 'bg-green-500 hover:bg-green-600';
            default:
                return '';
        }
    };

    const getRiskColor = (likelihood: string) => {
        switch (likelihood) {
            case 'High':
                return 'bg-red-500 hover:bg-red-600';
            case 'Medium':
                return 'bg-yellow-500 hover:bg-yellow-600';
            case 'Low':
                return 'bg-green-500 hover:bg-green-600';
            default:
                return '';
        }
    };

    const handleRowClick = (id: string) => {
        router.push(`/cases/${id}`);
    };

    const handleSort = (field: SortField) => {
        if (sortField === field) {
            setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
        } else {
            setSortField(field);
            setSortDirection('asc');
        }
    };

    const formatDate = (dateString: string) => {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
        });
    };

    const SortIcon = ({ field }: { field: SortField }) => {
        if (sortField !== field) return null;
        return sortDirection === 'asc' ? (
            <ArrowUp className='ml-1 h-4 w-4 inline' />
        ) : (
            <ArrowDown className='ml-1 h-4 w-4 inline' />
        );
    };

    return (
        <div className='border rounded-md'>
            <Table>
                <TableHeader>
                    <TableRow>
                        <TableHead>
                            <Button
                                variant='ghost'
                                className='p-0 font-medium'
                                onClick={() => handleSort('title')}
                            >
                                Case <SortIcon field='title' />
                            </Button>
                        </TableHead>
                        <TableHead>
                            <Button
                                variant='ghost'
                                className='p-0 font-medium'
                                onClick={() => handleSort('status')}
                            >
                                Status <SortIcon field='status' />
                            </Button>
                        </TableHead>
                        <TableHead>
                            <Button
                                variant='ghost'
                                className='p-0 font-medium'
                                onClick={() => handleSort('jurisdiction')}
                            >
                                Jurisdiction <SortIcon field='jurisdiction' />
                            </Button>
                        </TableHead>
                        <TableHead>
                            <Button
                                variant='ghost'
                                className='p-0 font-medium'
                                onClick={() => handleSort('caseType')}
                            >
                                Case Type <SortIcon field='caseType' />
                            </Button>
                        </TableHead>
                        <TableHead>
                            <Button
                                variant='ghost'
                                className='p-0 font-medium'
                                onClick={() => handleSort('date')}
                            >
                                Date <SortIcon field='date' />
                            </Button>
                        </TableHead>
                        <TableHead>
                            <Button
                                variant='ghost'
                                className='p-0 font-medium'
                                onClick={() => handleSort('brandImpact')}
                            >
                                Brand Impact <SortIcon field='brandImpact' />
                            </Button>
                        </TableHead>
                        <TableHead>
                            <Button
                                variant='ghost'
                                className='p-0 font-medium'
                                onClick={() => handleSort('risk')}
                            >
                                Risk <SortIcon field='risk' />
                            </Button>
                        </TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {loading ? (
                        <TableRow>
                            <TableCell
                                colSpan={7}
                                className='text-center py-6 text-muted-foreground'
                            >
                                Loading cases...
                            </TableCell>
                        </TableRow>
                    ) : sortedCases.length > 0 ? (
                        sortedCases.map((caseItem) => (
                            <TableRow
                                key={caseItem.id}
                                className='cursor-pointer hover:bg-muted/50'
                                onClick={() => handleRowClick(caseItem.id)}
                            >
                                <TableCell className='font-medium'>
                                    {caseItem.title}
                                </TableCell>
                                <TableCell>
                                    <Badge
                                        className={getStatusColor(
                                            caseItem.status as CaseStatus
                                        )}
                                    >
                                        {caseItem.status
                                            .charAt(0)
                                            .toUpperCase() +
                                            caseItem.status.slice(1)}
                                    </Badge>
                                </TableCell>
                                <TableCell>{caseItem.jurisdiction}</TableCell>
                                <TableCell>{caseItem.caseType}</TableCell>
                                <TableCell>
                                    {formatDate(caseItem.date)}
                                </TableCell>
                                <TableCell>
                                    {caseItem.brandImpactEstimate &&
                                        caseItem.brandImpactEstimate.impact !==
                                            'Not specified' && (
                                            <Badge
                                                className={getBrandImpactColor(
                                                    caseItem.brandImpactEstimate
                                                        .impact
                                                )}
                                            >
                                                {
                                                    caseItem.brandImpactEstimate
                                                        .impact
                                                }
                                            </Badge>
                                        )}
                                </TableCell>
                                <TableCell>
                                    {caseItem.caseWinLikelihood &&
                                        caseItem.status &&
                                        caseItem.status
                                            .toLowerCase()
                                            .includes('in progress') && (
                                            <Badge
                                                className={
                                                    parseFloat(
                                                        caseItem
                                                            .caseWinLikelihood
                                                            .percentage
                                                    ) < 50
                                                        ? 'bg-yellow-500 hover:bg-yellow-600'
                                                        : 'bg-green-500 hover:bg-green-600'
                                                }
                                            >
                                                {parseFloat(
                                                    caseItem.caseWinLikelihood
                                                        .percentage
                                                ) < 50
                                                    ? 'Likely to loose'
                                                    : 'Likely to win'}
                                            </Badge>
                                        )}
                                </TableCell>
                            </TableRow>
                        ))
                    ) : (
                        <TableRow>
                            <TableCell
                                colSpan={7}
                                className='text-center py-6 text-muted-foreground'
                            >
                                No cases found matching your search.
                            </TableCell>
                        </TableRow>
                    )}
                </TableBody>
            </Table>
        </div>
    );
}
