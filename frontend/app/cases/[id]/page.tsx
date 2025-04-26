'use client';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ArrowLeft, AlertCircle, CheckCircle, Clock, Info } from 'lucide-react';
import Link from 'next/link';
import { TopNavigation } from '@/components/top-navigation';
import { Timeline } from '@/components/timeline';
import { ArgumentationSection } from '@/components/argumentation-section';
import { OutcomePrediction } from '@/components/outcome-prediction';

// Mock data for a single case
const mockCaseData = {
    '1': {
        id: '1',
        title: 'Smith v. Bayersche Motors',
        status: 'won',
        jurisdiction: 'California',
        caseType: 'Liability',
        date: '2023-05-15',
        relevantLaws: [
            'California Vehicle Code § 27315',
            'California Civil Code § 1793.2',
        ],
        timeline: [
            {
                date: '2023-01-10',
                event: 'Initial complaint filed',
                description:
                    'Plaintiff filed complaint alleging faulty braking system',
            },
            {
                date: '2023-02-15',
                event: 'Response filed',
                description:
                    'Bayersche Motors filed response denying allegations',
            },
            {
                date: '2023-03-20',
                event: 'Discovery phase',
                description: 'Exchange of documents and expert testimonies',
            },
            {
                date: '2023-04-25',
                event: 'Court hearing',
                description: 'Judge ruled in favor of Bayersche Motors',
            },
            {
                date: '2023-05-15',
                event: 'Case closed',
                description: 'Case officially closed with favorable outcome',
            },
        ],
        offenseArgumentation:
            'The plaintiff claimed that the braking system in the Model S was defective, causing a collision. They argued that Bayersche Motors was aware of the defect but failed to issue a recall or properly warn customers.',
        defenseArgumentation:
            'Our defense demonstrated that the braking system met all safety standards and that the collision was caused by driver error rather than any defect in the vehicle. Expert testimony confirmed the braking system functioned as designed.',
        suggestions: [
            'Reference the Johnson v. AutoCorp case where similar claims were dismissed',
            "Include more technical data from the vehicle's diagnostic system",
            "Emphasize driver training requirements in the owner's manual",
        ],
        outcomePrediction: {
            cost: '$150,000 - $250,000',
            reputationalLoss: 'Low',
            winProbability: '85%',
        },
    },
    '2': {
        id: '2',
        title: 'Johnson Family Trust v. Bayersche',
        status: 'lost',
        jurisdiction: 'New York',
        caseType: 'Liability',
        date: '2023-08-22',
        relevantLaws: [
            'New York Vehicle and Traffic Law § 375',
            'New York General Business Law § 349',
        ],
        timeline: [
            {
                date: '2023-03-05',
                event: 'Initial complaint filed',
                description:
                    'Plaintiff alleged engine defect causing fire hazard',
            },
            {
                date: '2023-04-12',
                event: 'Response filed',
                description: 'Bayersche filed response contesting allegations',
            },
            {
                date: '2023-05-20',
                event: 'Expert testimony',
                description: 'Expert witnesses testified about engine design',
            },
            {
                date: '2023-07-15',
                event: 'Court ruling',
                description: 'Court ruled in favor of plaintiff',
            },
            {
                date: '2023-08-22',
                event: 'Case closed',
                description: 'Settlement finalized and case closed',
            },
        ],
        offenseArgumentation:
            'The plaintiff argued that the engine design in the Model X had a fundamental flaw that created a fire risk. They presented evidence of similar incidents and claimed Bayersche was negligent in addressing known issues.',
        defenseArgumentation:
            'Our defense argued that the isolated incidents were due to improper maintenance rather than design flaws. We presented extensive testing data showing the engine design met all safety standards.',
        suggestions: [
            'Consider early settlement in similar cases to avoid negative publicity',
            'Strengthen evidence of customer maintenance records',
            'Develop more comprehensive expert testimony on engine safety features',
        ],
        outcomePrediction: {
            cost: '$750,000 - $1,200,000',
            reputationalLoss: 'High',
            winProbability: '30%',
        },
    },
    '3': {
        id: '3',
        title: 'Martinez Product Liability Claim',
        status: 'in progress',
        jurisdiction: 'Texas',
        caseType: 'Liability',
        date: '2024-01-10',
        relevantLaws: [
            'Texas Transportation Code § 547.004',
            'Texas Deceptive Trade Practices Act',
        ],
        timeline: [
            {
                date: '2023-11-15',
                event: 'Initial complaint filed',
                description: 'Plaintiff alleges suspension system failure',
            },
            {
                date: '2023-12-20',
                event: 'Response filed',
                description: 'Bayersche filed response denying allegations',
            },
            {
                date: '2024-01-10',
                event: 'Discovery phase initiated',
                description: 'Exchange of documents and evidence begins',
            },
        ],
        offenseArgumentation:
            'The plaintiff claims that the suspension system in the Model Y failed during normal driving conditions, causing a rollover accident. They argue that Bayersche was aware of design flaws but failed to address them.',
        defenseArgumentation:
            "Our defense is focusing on the vehicle's maintenance history and road conditions at the time of the incident. We are gathering evidence to show the suspension system met all safety standards and was not defective.",
        suggestions: [
            'Reference the Williams v. AutoTech case where similar claims were successfully defended',
            'Obtain detailed road condition reports from the accident scene',
            'Commission independent testing of the specific suspension components',
        ],
        outcomePrediction: {
            cost: '$300,000 - $500,000',
            reputationalLoss: 'Medium',
            winProbability: '60%',
        },
    },
    '4': {
        id: '4',
        title: 'Williams Class Action',
        status: 'in progress',
        jurisdiction: 'Florida',
        caseType: 'Liability',
        date: '2024-02-28',
        relevantLaws: [
            'Florida Motor Vehicle Safety Act',
            'Florida Deceptive and Unfair Trade Practices Act',
        ],
        timeline: [
            {
                date: '2024-01-05',
                event: 'Class action filed',
                description:
                    'Group of plaintiffs filed class action regarding electrical system',
            },
            {
                date: '2024-02-10',
                event: 'Motion to dismiss',
                description:
                    'Bayersche filed motion to dismiss the class action',
            },
            {
                date: '2024-02-28',
                event: 'Motion denied',
                description: 'Court denied motion to dismiss, case proceeding',
            },
        ],
        offenseArgumentation:
            'The class action alleges that the electrical system in multiple Bayersche models has a defect that causes unexpected power loss. Plaintiffs claim this creates a safety hazard and that Bayersche concealed the issue.',
        defenseArgumentation:
            'Our defense strategy is to challenge the class certification by demonstrating the diversity of electrical systems across different models and years. We are also gathering data to show the reported incidents are isolated and not indicative of a systemic defect.',
        suggestions: [
            'Consider partial settlement for older models while contesting newer ones',
            'Develop stronger evidence of system improvements over time',
            'Emphasize the low incident rate compared to total vehicles sold',
        ],
        outcomePrediction: {
            cost: '$2,000,000 - $5,000,000',
            reputationalLoss: 'High',
            winProbability: '45%',
        },
    },
    '5': {
        id: '5',
        title: 'Garcia v. Bayersche Manufacturing',
        status: 'won',
        jurisdiction: 'Michigan',
        caseType: 'Liability',
        date: '2023-11-05',
        relevantLaws: [
            'Michigan Vehicle Code',
            'Michigan Consumer Protection Act',
        ],
        timeline: [
            {
                date: '2023-06-12',
                event: 'Initial complaint filed',
                description: 'Plaintiff alleged transmission defect',
            },
            {
                date: '2023-07-18',
                event: 'Response filed',
                description: 'Bayersche filed response with counterclaims',
            },
            {
                date: '2023-09-25',
                event: 'Expert testimony',
                description:
                    'Expert witnesses testified about transmission design',
            },
            {
                date: '2023-10-30',
                event: 'Court ruling',
                description: 'Court ruled in favor of Bayersche',
            },
            {
                date: '2023-11-05',
                event: 'Case closed',
                description: 'Case officially closed with favorable outcome',
            },
        ],
        offenseArgumentation:
            'The plaintiff claimed that the transmission in their Model Z was defective, causing unexpected shifting and safety hazards. They argued that Bayersche was aware of the issue but failed to address it properly.',
        defenseArgumentation:
            "Our defense successfully demonstrated that the transmission functioned as designed and that the plaintiff's issues were due to improper use of the vehicle. We presented extensive testing data and expert testimony to support our position.",
        suggestions: [
            'Use similar technical evidence approach in future transmission cases',
            'Develop educational materials for customers about proper transmission use',
            'Consider proactive service bulletins for similar customer complaints',
        ],
        outcomePrediction: {
            cost: '$200,000 - $300,000',
            reputationalLoss: 'Low',
            winProbability: '80%',
        },
    },
};

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
    const caseData = mockCaseData[params.id as keyof typeof mockCaseData];

    if (!caseData) {
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
                            The case you're looking for doesn't exist.
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
                                            (law, index) => (
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
