'use client';

import { useState, useEffect } from 'react';
import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    Legend,
    PieChart,
    Pie,
    Cell,
} from 'recharts';
import { fetchStatusStats } from '@/lib/api';

// Map status to color
const STATUS_COLORS: Record<string, string> = {
    'In favour of defendant': '#22c55e', // green
    'In favour of plaintiff': '#ef4444', // red
    'In progress': '#2563eb', // standard blue
};

export function CaseStatusChart() {
    const [statusData, setStatusData] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function loadStatusData() {
            setLoading(true);
            try {
                const data = await fetchStatusStats();
                if (data && data.length > 0) {
                    setStatusData(data);
                }
            } catch (error) {
                console.error('Error loading status stats:', error);
            } finally {
                setLoading(false);
            }
        }

        loadStatusData();
    }, []);

    if (loading) {
        return (
            <div className='flex items-center justify-center h-full'>
                Loading data...
            </div>
        );
    }

    return (
        <div className='grid grid-cols-1 gap-6 h-full'>
            <ResponsiveContainer width='100%' height='100%'>
                <PieChart>
                    <Pie
                        data={statusData}
                        dataKey='count'
                        nameKey='status'
                        cx='50%'
                        cy='50%'
                        outerRadius={80}
                        label={({ status, count, percent }) =>
                            `${status}: ${count} (${(percent * 100).toFixed(
                                0
                            )}%)`
                        }
                    >
                        {statusData.map((entry, index) => (
                            <Cell
                                key={`cell-${index}`}
                                fill={STATUS_COLORS[entry.status] || '#8884d8'}
                            />
                        ))}
                    </Pie>
                    <Tooltip formatter={(value, name) => [value, name]} />
                    <Legend />
                </PieChart>
            </ResponsiveContainer>
        </div>
    );
}
