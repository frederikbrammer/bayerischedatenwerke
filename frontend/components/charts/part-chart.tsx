'use client';

import { useState, useEffect } from 'react';
import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
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

    return (
        <ResponsiveContainer width='100%' height='100%'>
            <BarChart
                data={partData}
                layout='vertical'
                margin={{
                    top: 20,
                    right: 30,
                    left: 120,
                    bottom: 5,
                }}
            >
                <CartesianGrid strokeDasharray='3 3' />
                <XAxis type='number' />
                <YAxis dataKey='part' type='category' width={100} />
                <Tooltip />
                <Legend />
                <Bar dataKey='count' fill='#8b5cf6' name='Cases' />
            </BarChart>
        </ResponsiveContainer>
    );
}
