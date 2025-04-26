import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface TimelineEvent {
    date: string;
    event: string;
    description: string;
}

interface TimelineProps {
    events: TimelineEvent[];
}

export function Timeline({ events }: TimelineProps) {
    const formatDate = (dateString: string) => {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
        });
    };

    return (
        <Card>
            <CardHeader>
                <CardTitle>Case Timeline</CardTitle>
            </CardHeader>
            <CardContent>
                <div className='relative border-l border-muted pl-6 ml-3'>
                    {events.map((event, index) => (
                        <div key={index} className='mb-8 relative'>
                            <div className='absolute -left-[32.5px] mt-1.5 h-4 w-4 rounded-full border border-muted bg-gray-400'></div>
                            <time className='mb-1 text-sm font-normal leading-none text-muted-foreground'>
                                {formatDate(event.date)}
                            </time>
                            <h3 className='text-lg font-semibold'>
                                {event.event}
                            </h3>
                            <p className='text-sm text-muted-foreground'>
                                {event.description}
                            </p>
                        </div>
                    ))}
                </div>
            </CardContent>
        </Card>
    );
}
