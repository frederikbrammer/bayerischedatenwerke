'use client';

import { useState, useEffect } from 'react';
import {
    PieChart,
    Pie,
    Cell,
    Legend,
    Tooltip,
    ResponsiveContainer,
} from 'recharts';
import { fetchCarStats } from '@/lib/api';

const COLORS = ['#3b82f6', '#8b5cf6', '#ec4899', '#f97316', '#10b981'];

export function CarChart() {
    const [carData, setCarData] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function loadCarData() {
            setLoading(true);
            try {
                const data = await fetchCarStats();
                if (data && data.length > 0) {
                    setCarData(data);
                }
            } catch (error) {
                console.error('Error loading car stats:', error);
            } finally {
                setLoading(false);
            }
        }

        loadCarData();
    }, []);

    if (loading) {
        return (
            <div className='flex items-center justify-center h-full'>
                Loading data...
            </div>
        );
    }

    return (
        <ResponsiveContainer width='100%' height='100%'>
            <PieChart>
                <Pie
                    data={carData}
                    dataKey='count'
                    nameKey='model'
                    cx='50%'
                    cy='50%'
                    outerRadius={80}
                    label={({ model, count, percent }) =>
                        `${model}: ${count} (${(percent * 100).toFixed(0)}%)`
                    }
                >
                    {carData.map((entry, index) => (
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
    );
}
