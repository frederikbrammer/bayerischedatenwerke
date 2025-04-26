'use client';

import { useState, useEffect } from 'react';
import {
    PieChart,
    Pie,
    Cell,
    Tooltip,
    Legend,
    ResponsiveContainer,
} from 'recharts';
import { fetchPartStats } from '@/lib/api';

export function PartChart() {
    const [partData, setPartData] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function loadPartData() {
            setLoading(true);
            try {
                const data = await fetchPartStats();
                if (data && data.length > 0) {
                    setPartData(data);
                }
            } catch (error) {
                console.error('Error loading part stats:', error);
            } finally {
                setLoading(false);
            }
        }

        loadPartData();
    }, []);

    if (loading) {
        return (
            <div className='flex items-center justify-center h-full'>
                Loading data...
            </div>
        );
    }

    // Colors for the pie chart slices
    const COLORS = [
        '#8b5cf6',
        '#6366f1',
        '#a855f7',
        '#ec4899',
        '#f43f5e',
        '#f97316',
        '#facc15',
    ];

    return (
        <ResponsiveContainer width='100%' height='100%'>
            <PieChart>
                <Pie
                    data={partData}
                    dataKey='count'
                    nameKey='part'
                    cx='50%'
                    cy='50%'
                    outerRadius={120}
                    label={({ name, percent }) =>
                        `${name}: ${(percent * 100).toFixed(0)}%`
                    }
                    labelLine={true}
                >
                    {partData.map((entry, index) => (
                        <Cell
                            key={`cell-${index}`}
                            fill={COLORS[index % COLORS.length]}
                        />
                    ))}
                </Pie>
                <Tooltip
                    formatter={(value, name, props) => [
                        `${value} cases`,
                        props.payload.part,
                    ]}
                />
                <Legend />
            </PieChart>
        </ResponsiveContainer>
    );
}
