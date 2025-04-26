import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';

interface OutcomePredictionProps {
    prediction?: {
        cost: string;
        reputationalLoss: string;
        winProbability: string;
    } | null;
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

    const winProbabilityValue = Number.parseInt(
        prediction.winProbability.replace('%', '')
    );

    return (
        <div className='grid grid-cols-1 md:grid-cols-2 gap-6'>
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
                                {prediction.cost}
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
                                    value={winProbabilityValue}
                                    className='h-2'
                                />
                                <span className='text-sm font-medium'>
                                    {prediction.winProbability}
                                </span>
                            </div>
                        </div>
                    </div>
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <CardTitle>Reputational Impact</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className='flex flex-col items-center justify-center h-full'>
                        <h3 className='text-sm font-medium mb-2'>
                            Estimated Reputational Loss
                        </h3>
                        <p
                            className={`text-3xl font-bold ${getReputationalLossColor(
                                prediction.reputationalLoss
                            )}`}
                        >
                            {prediction.reputationalLoss}
                        </p>
                        <p className='text-xs text-muted-foreground mt-4 text-center'>
                            Based on media coverage analysis, social media
                            sentiment, and industry impact
                        </p>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
