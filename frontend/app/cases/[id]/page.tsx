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

type CaseStatus =
    | 'in favour of defendant'
    | 'in favour of plaintiff'
    | 'settled'
    | 'in progress first instance'
    | 'dismissed'
    | 'in progress appeal'
    | 'in progress supreme court';

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

const getStatusIcon = (status: CaseStatus) => {
    const status_lower = status.toLowerCase();
    if (status_lower.includes('in progress')) {
        return <Clock className='h-5 w-5 text-blue-500' />;
    }

    switch (status_lower) {
        case 'in favour of defendant':
            return <CheckCircle className='h-5 w-5 text-green-500' />;
        case 'in favour of plaintiff':
            return <AlertCircle className='h-5 w-5 text-red-500' />;
        case 'settled':
            return <Clock className='h-5 w-5 text-yellow-500' />;
        case 'dismissed':
            return <Info className='h-5 w-5 text-gray-500' />;
        default:
            return <Info className='h-5 w-5 text-gray-300' />;
    }
};

export default function CaseDetailPage({
    params,
}: {
    params: Promise<{ id: string }>;
}) {
    const { id: caseId } = React.use(params);

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
                    <div className='text-center py-12'></div>
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

                <div className='flex flex-col items-left mb-6'>
                    <div>
                        <h1 className='text-3xl font-bold'>{caseData.title}</h1>
                        <p className='text-muted-foreground'>
                            Filed on {formatDate(caseData.date)}
                        </p>
                    </div>
                    <div className='flex items-center justify-between pt-2 w-full'>
                        <div className='flex gap-2'>
                            {caseData.caseWinLikelihood &&
                                caseData.status
                                    .toLowerCase()
                                    .includes('in progress') && (
                                    <Badge
                                        className={
                                            parseFloat(
                                                caseData.caseWinLikelihood
                                                    .percentage
                                            ) < 50
                                                ? 'bg-yellow-500 hover:bg-yellow-600'
                                                : 'bg-green-500 hover:bg-green-600'
                                        }
                                    >
                                        {parseFloat(
                                            caseData.caseWinLikelihood
                                                .percentage
                                        ) < 50
                                            ? 'Likely to loose'
                                            : 'Likely to win'}
                                    </Badge>
                                )}
                            {caseData.brandImpactEstimate && (
                                <Badge
                                    className={
                                        caseData.brandImpactEstimate.impact ===
                                        'High'
                                            ? 'bg-red-500 hover:bg-red-600'
                                            : caseData.brandImpactEstimate
                                                  .impact === 'Medium'
                                            ? 'bg-yellow-500 hover:bg-yellow-600'
                                            : 'bg-green-500 hover:bg-green-600'
                                    }
                                >
                                    Brand Impact:{' '}
                                    {caseData.brandImpactEstimate.impact}
                                </Badge>
                            )}
                            <Badge
                                className={getStatusColor(
                                    caseData.status as CaseStatus
                                )}
                            >
                                {caseData.status.charAt(0).toUpperCase() +
                                    caseData.status.slice(1)}
                            </Badge>
                        </div>
                        <div className='flex gap-2'>
                            <Button
                                variant='default'
                                size='sm'
                                className='bg-black hover:bg-black text-white'
                            >
                                <span className='flex items-center gap-1'>
                                    <svg
                                        xmlns='http://www.w3.org/2000/svg'
                                        width='16'
                                        height='16'
                                        fill='none'
                                        viewBox='0 0 24 24'
                                    >
                                        <path
                                            stroke='currentColor'
                                            strokeWidth='2'
                                            strokeLinecap='round'
                                            strokeLinejoin='round'
                                            d='M12 5v14m7-7H5'
                                        />
                                    </svg>
                                    Upload document
                                </span>
                            </Button>
                            <Button
                                variant='secondary'
                                size='sm'
                                className='text-black dark:text-white border border-gray-300 dark:border-gray-700'
                            >
                                <span className='flex items-center gap-1'>
                                    <svg
                                        xmlns='http://www.w3.org/2000/svg'
                                        width='16'
                                        height='16'
                                        fill='none'
                                        viewBox='0 0 24 24'
                                    >
                                        <path
                                            d='M12 17h.01'
                                            stroke='currentColor'
                                            strokeWidth='2'
                                            strokeLinecap='round'
                                        />
                                        <path
                                            d='M12 13a3 3 0 1 0-3-3'
                                            stroke='currentColor'
                                            strokeWidth='2'
                                            strokeLinecap='round'
                                            strokeLinejoin='round'
                                        />
                                        <circle
                                            cx='12'
                                            cy='12'
                                            r='10'
                                            stroke='currentColor'
                                            strokeWidth='2'
                                        />
                                    </svg>
                                    Ask Question
                                </span>
                            </Button>
                        </div>
                    </div>
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
                                        <dt className='font-medium'>
                                            Harm type:
                                        </dt>
                                        <dd>{caseData.harmType}</dd>
                                        <dt className='font-medium'>Cause:</dt>
                                        <dd>{caseData.cause}</dd>
                                        <dt className='font-medium'>
                                            Case Summary:
                                        </dt>
                                        <dd>{caseData.caseSummary}</dd>
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
                        </CardContent>
                    </Card>

                    {/* Timeline Section */}
                    <Timeline events={caseData.timeline} />

                    {/* Case Analysis Section - New Section for Additional Data */}
                    <Card>
                        <CardHeader>
                            <CardTitle>Case Details</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className='grid grid-cols-1 md:grid-cols-2 gap-6'>
                                <div>
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
                                                    {caseData.timeToResolutionMonths ===
                                                    'Not specified'
                                                        ? 'Unknown'
                                                        : `${caseData.timeToResolutionMonths} months`}
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
                                        {caseData.affectedCar &&
                                            caseData.affectedCar !==
                                                'Not specified' && (
                                                <>
                                                    <dt className='font-medium'>
                                                        Affected Car:
                                                    </dt>
                                                    <dd>
                                                        {caseData.affectedCar}
                                                    </dd>
                                                </>
                                            )}

                                        {caseData.affectedPart &&
                                            caseData.affectedPart !==
                                                'Not specified' && (
                                                <>
                                                    <dt className='font-medium'>
                                                        Affected Part:
                                                    </dt>
                                                    <dd>
                                                        {caseData.affectedPart}
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
                                                        <Badge
                                                            className={
                                                                caseData
                                                                    .mediaCoverageLevel
                                                                    .level ===
                                                                'High'
                                                                    ? 'bg-red-500 hover:bg-red-600'
                                                                    : caseData
                                                                          .mediaCoverageLevel
                                                                          .level ===
                                                                      'Medium'
                                                                    ? 'bg-yellow-500 hover:bg-yellow-600'
                                                                    : 'bg-green-500 hover:bg-green-600'
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
                                                        <Badge
                                                            className={
                                                                caseData
                                                                    .expectedBrandImpact
                                                                    .impact ===
                                                                'High'
                                                                    ? 'bg-red-500 hover:bg-red-600'
                                                                    : caseData
                                                                          .expectedBrandImpact
                                                                          .impact ===
                                                                      'Medium'
                                                                    ? 'bg-yellow-500 hover:bg-yellow-600'
                                                                    : 'bg-green-500 hover:bg-green-600'
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
                                    caseData.plaintiffArgumentation
                                }
                                defenseArgumentation={
                                    caseData.defenseArgumentation
                                }
                            />
                        </CardContent>
                    </Card>

                    {/* Evidence Section */}
                    <Card>
                        <CardHeader>
                            <CardTitle>Evidence</CardTitle>
                        </CardHeader>
                        <CardContent>
                            {Array.isArray(caseData.evidence) &&
                            caseData.evidence.length > 0 ? (
                                <ul className='space-y-3'>
                                    {caseData.evidence.map(
                                        (ev: any, idx: number) => (
                                            <li
                                                key={idx}
                                                className='border rounded p-3 bg-gray-50 dark:bg-gray-800'
                                            >
                                                <p className='text-sm mb-1'>
                                                    <span className='font-medium'>
                                                        Text:
                                                    </span>{' '}
                                                    {ev.text}
                                                </p>
                                                <p className='text-sm mb-1'>
                                                    <span className='font-medium'>
                                                        Relevance:
                                                    </span>{' '}
                                                    {ev.relevance}
                                                </p>
                                                <div className='flex items-center gap-2'>
                                                    <span className='font-medium'>
                                                        Strength:
                                                    </span>
                                                    <Badge
                                                        className={
                                                            ev.strength ===
                                                            'strong'
                                                                ? 'bg-primary text-primary-foreground'
                                                                : ev.strength ===
                                                                  'moderate'
                                                                ? 'bg-secondary text-secondary-foreground'
                                                                : 'border border-input bg-background text-foreground'
                                                        }
                                                    >
                                                        {ev.strength
                                                            .charAt(0)
                                                            .toUpperCase() +
                                                            ev.strength.slice(
                                                                1
                                                            )}
                                                    </Badge>
                                                </div>
                                            </li>
                                        )
                                    )}
                                </ul>
                            ) : (
                                <p className='text-sm text-muted-foreground'>
                                    No evidence listed for this case.
                                </p>
                            )}
                        </CardContent>
                    </Card>

                    {/* Case Law Section */}
                    <Card>
                        <CardHeader>
                            <CardTitle>Case Law</CardTitle>
                        </CardHeader>
                        <CardContent>
                            {caseData.similarCases &&
                            caseData.similarCases.length > 0 ? (
                                <ul className='list-disc pl-5 space-y-1'>
                                    {caseData.similarCases.map(
                                        (related: any, idx: number) => (
                                            <li key={idx} className='text-sm'>
                                                <Link
                                                    href={`/cases/${related}`}
                                                    className='text-blue-600 hover:underline'
                                                >
                                                    {related}
                                                </Link>
                                            </li>
                                        )
                                    )}
                                </ul>
                            ) : (
                                <p className='text-sm text-muted-foreground'>
                                    No case law found for this case.
                                </p>
                            )}
                        </CardContent>
                    </Card>

                    {/* Outcome Prediction Section */}
                    {caseData.status &&
                        caseData.status
                            .toLowerCase()
                            .includes('in progress') && (
                            <Card>
                                <CardHeader>
                                    <CardTitle>Outcome Prediction</CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <OutcomePrediction
                                        prediction={caseData.caseWinLikelihood}
                                    />
                                </CardContent>
                            </Card>
                        )}
                </div>
            </div>
        </>
    );
}
