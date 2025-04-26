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

// Mock data for yearly trend (API doesn't provide this yet)
const yearlyData = [
    { name: '2020', won: 15, lost: 8, inProgress: 2 },
    { name: '2021', won: 18, lost: 7, inProgress: 3 },
    { name: '2022', won: 22, lost: 9, inProgress: 4 },
    { name: '2023', won: 23, lost: 8, inProgress: 6 },
    { name: '2024', won: 0, lost: 0, inProgress: 17 },
];

// Colors for the status pie chart
const COLORS = ['#22c55e', '#ef4444', '#3b82f6'];

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
                                fill={COLORS[index % COLORS.length]}
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
