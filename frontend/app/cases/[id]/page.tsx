'use client';

import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ArrowLeft, AlertCircle, CheckCircle, Clock, Info } from 'lucide-react';
import Link from 'next/link';
import { TopNavigation } from '@/components/top-navigation';
import { Timeline } from '@/components/timeline';
import { ArgumentationSection } from '@/components/argumentation-section';
import { OutcomePrediction } from '@/components/outcome-prediction';
import { fetchCaseById } from '@/lib/api';

type CaseStatus = 'won' | 'lost' | 'in progress';

const getStatusColor = (status: CaseStatus) => {
    switch (status) {
        case 'won':
            return 'bg-green-500 hover:bg-green-600';
        case 'lost':
            return 'bg-red-500 hover:bg-red-600';
        case 'in progress':
            return 'bg-blue-500 hover:bg-blue-600';
        default:
            return '';
    }
};

const getStatusIcon = (status: CaseStatus) => {
    switch (status) {
        case 'won':
            return <CheckCircle className='h-5 w-5 text-green-500' />;
        case 'lost':
            return <AlertCircle className='h-5 w-5 text-red-500' />;
        case 'in progress':
            return <Clock className='h-5 w-5 text-blue-500' />;
        default:
            return <Info className='h-5 w-5' />;
    }
};

export default function CaseDetailPage({ params }: { params: { id: string } }) {
    // Unwrap params using React.use()
    const unwrappedParams = React.use(params);
    const caseId = unwrappedParams.id;

    const [caseData, setCaseData] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        async function loadCase() {
            setLoading(true);
            try {
                const data = await fetchCaseById(caseId);
                if (data) {
                    setCaseData(data);
                } else {
                    setError('Case not found');
                }
            } catch (err) {
                setError('Failed to load case data');
                console.error(err);
            } finally {
                setLoading(false);
            }
        }

        loadCase();
    }, [caseId]);

    if (loading) {
        return (
            <>
                <TopNavigation />
                <div className='container mx-auto p-6'>
                    <div className='text-center py-12'>
                        <h1 className='text-2xl font-bold mb-2'>Loading...</h1>
                    </div>
                </div>
            </>
        );
    }

    if (error || !caseData) {
        return (
            <>
                <TopNavigation />
                <div className='container mx-auto p-6'>
                    <div className='mb-6'>
                        <Button asChild variant='outline' size='sm'>
                            <Link href='/cases'>
                                <ArrowLeft className='mr-2 h-4 w-4' /> Back to
                                Cases
                            </Link>
                        </Button>
                    </div>
                    <div className='text-center py-12'>
                        <h1 className='text-2xl font-bold mb-2'>
                            Case Not Found
                        </h1>
                        <p className='text-muted-foreground'>
                            {error ||
                                "The case you're looking for doesn't exist."}
                        </p>
                    </div>
                </div>
            </>
        );
    }

    const formatDate = (dateString: string) => {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
        });
    };

    return (
        <>
            <TopNavigation />
            <div className='container mx-auto p-6'>
                <div className='mb-6'>
                    <Button asChild variant='outline' size='sm'>
                        <Link href='/cases'>
                            <ArrowLeft className='mr-2 h-4 w-4' /> Back to Cases
                        </Link>
                    </Button>
                </div>

                <div className='flex justify-between items-center mb-6'>
                    <div>
                        <h1 className='text-3xl font-bold'>{caseData.title}</h1>
                        <p className='text-muted-foreground'>
                            Filed on {formatDate(caseData.date)}
                        </p>
                    </div>
                    <Badge
                        className={getStatusColor(
                            caseData.status as CaseStatus
                        )}
                    >
                        {caseData.status.charAt(0).toUpperCase() +
                            caseData.status.slice(1)}
                    </Badge>
                </div>

                <div className='space-y-8'>
                    {/* Overview Section */}
                    <Card>
                        <CardHeader>
                            <CardTitle>General Case Information</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className='grid grid-cols-1 md:grid-cols-2 gap-6'>
                                <div>
                                    <dl className='grid grid-cols-2 gap-4'>
                                        <dt className='font-medium'>
                                            Case ID:
                                        </dt>
                                        <dd>{caseData.id}</dd>
                                        <dt className='font-medium'>
                                            Jurisdiction:
                                        </dt>
                                        <dd>{caseData.jurisdiction}</dd>
                                        <dt className='font-medium'>
                                            Case Type:
                                        </dt>
                                        <dd>{caseData.caseType}</dd>
                                        <dt className='font-medium'>Status:</dt>
                                        <dd className='flex items-center gap-2'>
                                            {getStatusIcon(
                                                caseData.status as CaseStatus
                                            )}
                                            {caseData.status
                                                .charAt(0)
                                                .toUpperCase() +
                                                caseData.status.slice(1)}
                                        </dd>
                                        <dt className='font-medium'>
                                            Filed Date:
                                        </dt>
                                        <dd>{formatDate(caseData.date)}</dd>
                                    </dl>
                                </div>

                                <div>
                                    <h3 className='font-medium mb-2'>
                                        Relevant Laws:
                                    </h3>
                                    <ul className='list-disc pl-5 space-y-1'>
                                        {caseData.relevantLaws.map(
                                            (law: string, index: number) => (
                                                <li
                                                    key={index}
                                                    className='text-sm'
                                                >
                                                    {law}
                                                </li>
                                            )
                                        )}
                                    </ul>
                                </div>
                            </div>

                            <div className='mt-6'>
                                <h3 className='font-medium mb-2'>
                                    Case Summary:
                                </h3>
                                <p className='text-sm text-muted-foreground'>
                                    This case involves allegations related to
                                    the{' '}
                                    {caseData.title
                                        .toLowerCase()
                                        .includes('braking')
                                        ? 'braking system'
                                        : caseData.title
                                              .toLowerCase()
                                              .includes('engine')
                                        ? 'engine'
                                        : caseData.title
                                              .toLowerCase()
                                              .includes('suspension')
                                        ? 'suspension system'
                                        : caseData.title
                                              .toLowerCase()
                                              .includes('electrical')
                                        ? 'electrical system'
                                        : 'transmission'}{' '}
                                    in Bayersche vehicles. The plaintiff has
                                    filed a {caseData.caseType.toLowerCase()}{' '}
                                    claim in {caseData.jurisdiction}.
                                </p>
                            </div>
                        </CardContent>
                    </Card>

                    {/* Timeline Section */}
                    <Card>
                        <CardHeader>
                            <CardTitle>Timeline</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <Timeline events={caseData.timeline} />
                        </CardContent>
                    </Card>

                    {/* Case Analysis Section - New Section for Additional Data */}
                    <Card>
                        <CardHeader>
                            <CardTitle>Case Analysis</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className='grid grid-cols-1 md:grid-cols-2 gap-6'>
                                <div>
                                    <h3 className='font-medium mb-3'>
                                        Case Details
                                    </h3>
                                    <dl className='grid grid-cols-2 gap-3'>
                                        {caseData.defectType && (
                                            <>
                                                <dt className='font-medium'>
                                                    Defect Type:
                                                </dt>
                                                <dd>
                                                    {Array.isArray(
                                                        caseData.defectType
                                                    )
                                                        ? caseData.defectType.join(
                                                              ', '
                                                          )
                                                        : caseData.defectType}
                                                </dd>
                                            </>
                                        )}

                                        {caseData.numberOfClaimants && (
                                            <>
                                                <dt className='font-medium'>
                                                    Number of Claimants:
                                                </dt>
                                                <dd>
                                                    {caseData.numberOfClaimants}
                                                </dd>
                                            </>
                                        )}

                                        {caseData.timeToResolutionMonths && (
                                            <>
                                                <dt className='font-medium'>
                                                    Time to Resolution:
                                                </dt>
                                                <dd>
                                                    {
                                                        caseData.timeToResolutionMonths
                                                    }{' '}
                                                    months
                                                </dd>
                                            </>
                                        )}

                                        {caseData.settlementAmount &&
                                            caseData.settlementAmount !==
                                                'Not specified' && (
                                                <>
                                                    <dt className='font-medium'>
                                                        Settlement Amount:
                                                    </dt>
                                                    <dd>
                                                        {
                                                            caseData.settlementAmount
                                                        }
                                                    </dd>
                                                </>
                                            )}

                                        {caseData.defenseCostEstimate &&
                                            caseData.defenseCostEstimate !==
                                                'Not specified' && (
                                                <>
                                                    <dt className='font-medium'>
                                                        Defense Cost Estimate:
                                                    </dt>
                                                    <dd>
                                                        {
                                                            caseData.defenseCostEstimate
                                                        }
                                                    </dd>
                                                </>
                                            )}
                                    </dl>
                                </div>

                                <div>
                                    {caseData.mediaCoverageLevel &&
                                        typeof caseData.mediaCoverageLevel ===
                                            'object' && (
                                            <div className='mb-4'>
                                                <h3 className='font-medium mb-2'>
                                                    Media Coverage Assessment
                                                </h3>
                                                <div className='bg-gray-50 dark:bg-gray-800 p-3 rounded-lg'>
                                                    <div className='flex items-center gap-2 mb-2'>
                                                        <span className='font-medium'>
                                                            Level:
                                                        </span>
                                                        <Badge
                                                            variant={
                                                                caseData
                                                                    .mediaCoverageLevel
                                                                    .level ===
                                                                'High'
                                                                    ? 'destructive'
                                                                    : caseData
                                                                          .mediaCoverageLevel
                                                                          .level ===
                                                                      'Medium'
                                                                    ? 'warning'
                                                                    : 'outline'
                                                            }
                                                        >
                                                            {
                                                                caseData
                                                                    .mediaCoverageLevel
                                                                    .level
                                                            }
                                                        </Badge>
                                                    </div>
                                                    {caseData.mediaCoverageLevel
                                                        .explanation && (
                                                        <p className='text-sm text-muted-foreground'>
                                                            {
                                                                caseData
                                                                    .mediaCoverageLevel
                                                                    .explanation
                                                            }
                                                        </p>
                                                    )}
                                                </div>
                                            </div>
                                        )}

                                    {caseData.expectedBrandImpact &&
                                        typeof caseData.expectedBrandImpact ===
                                            'object' && (
                                            <div>
                                                <h3 className='font-medium mb-2'>
                                                    Expected Brand Impact
                                                </h3>
                                                <div className='bg-gray-50 dark:bg-gray-800 p-3 rounded-lg'>
                                                    <div className='flex items-center gap-2 mb-2'>
                                                        <span className='font-medium'>
                                                            Impact:
                                                        </span>
                                                        <Badge
                                                            variant={
                                                                caseData
                                                                    .expectedBrandImpact
                                                                    .impact ===
                                                                'High'
                                                                    ? 'destructive'
                                                                    : caseData
                                                                          .expectedBrandImpact
                                                                          .impact ===
                                                                      'Medium'
                                                                    ? 'warning'
                                                                    : 'outline'
                                                            }
                                                        >
                                                            {
                                                                caseData
                                                                    .expectedBrandImpact
                                                                    .impact
                                                            }
                                                        </Badge>
                                                    </div>
                                                    {caseData
                                                        .expectedBrandImpact
                                                        .explanation && (
                                                        <p className='text-sm text-muted-foreground'>
                                                            {
                                                                caseData
                                                                    .expectedBrandImpact
                                                                    .explanation
                                                            }
                                                        </p>
                                                    )}
                                                </div>
                                            </div>
                                        )}
                                </div>
                            </div>
                        </CardContent>
                    </Card>

                    {/* Argumentation Section */}
                    <Card>
                        <CardHeader>
                            <CardTitle>Argumentation</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <ArgumentationSection
                                offenseArgumentation={
                                    caseData.offenseArgumentation
                                }
                                defenseArgumentation={
                                    caseData.defenseArgumentation
                                }
                                suggestions={caseData.suggestions}
                            />
                        </CardContent>
                    </Card>

                    {/* Outcome Prediction Section */}
                    <Card>
                        <CardHeader>
                            <CardTitle>Outcome Prediction</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <OutcomePrediction
                                prediction={caseData.outcomePrediction}
                            />
                        </CardContent>
                    </Card>
                </div>
            </div>
        </>
    );
}
