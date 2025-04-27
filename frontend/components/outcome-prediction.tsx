import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';

interface OutcomePredictionProps {
    prediction?: any | null;
}

export function OutcomePrediction({ prediction }: OutcomePredictionProps) {
    // If prediction is null or undefined, show a placeholder
    if (!prediction) {
        return (
            <div className='p-4 text-center'>
                <p className='text-muted-foreground'>
                    No outcome prediction available for this case yet.
                </p>
            </div>
        );
    }

    const getReputationalLossColor = (level: string) => {
        switch (level.toLowerCase()) {
            case 'low':
                return 'text-green-600';
            case 'medium':
                return 'text-yellow-600';
            case 'high':
                return 'text-red-600';
            default:
                return '';
        }
    };

    return (
        <Card>
            <CardHeader>
                <CardTitle>Financial Impact</CardTitle>
            </CardHeader>
            <CardContent>
                <div className='space-y-4'>
                    <div>
                        <h3 className='text-sm font-medium mb-1'>
                            Estimated Cost
                        </h3>
                        <p className='text-2xl font-bold'>
                            $200,000 - $450,000
                        </p>
                        <p className='text-xs text-muted-foreground mt-1'>
                            Including legal fees, settlements, and
                            administrative costs
                        </p>
                    </div>

                    <div>
                        <h3 className='text-sm font-medium mb-1'>
                            Win Probability
                        </h3>
                        <div className='flex items-center gap-2'>
                            <Progress
                                value={prediction.percentage}
                                className='h-2'
                            />
                            <span className='text-sm font-medium w-20'>
                                {prediction.percentage} %
                            </span>
                        </div>
                    </div>

                    {/* Explanation Section */}
                    {prediction.explanation && (
                        <div className='mt-4'>
                            <p className='text-sm text-muted-foreground'>
                                {prediction.explanation}
                            </p>
                        </div>
                    )}

                    {/* Key Factors Section */}
                    {Array.isArray(prediction.keyFactors) &&
                        prediction.keyFactors.length > 0 && (
                            <div>
                                <h3 className='text-sm font-medium mb-1'>
                                    Key Factors
                                </h3>
                                <ul className='list-disc pl-5 space-y-1'>
                                    {prediction.keyFactors.map(
                                        (
                                            kf: {
                                                factor: string;
                                                impact: string;
                                            },
                                            idx: number
                                        ) => (
                                            <li key={idx}>
                                                <span className='font-medium'>
                                                    {kf.factor}
                                                </span>
                                                <span className='ml-2 text-xs text-muted-foreground'>
                                                    ({kf.impact})
                                                </span>
                                            </li>
                                        )
                                    )}
                                </ul>
                            </div>
                        )}
                </div>
            </CardContent>
        </Card>
    );
}
