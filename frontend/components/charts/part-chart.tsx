"use client"

import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from "recharts"

// Mock data for parts affected
const partData = [
  { name: "Braking System", value: 35 },
  { name: "Engine", value: 25 },
  { name: "Transmission", value: 18 },
  { name: "Suspension", value: 15 },
  { name: "Electrical System", value: 12 },
  { name: "Other", value: 22 },
]

const COLORS = ["#3b82f6", "#22c55e", "#eab308", "#ef4444", "#a855f7", "#94a3b8"]

export function PartChart() {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <PieChart>
        <Pie
          data={partData}
          cx="50%"
          cy="50%"
          labelLine={false}
          outerRadius={120}
          fill="#8884d8"
          dataKey="value"
          label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
        >
          {partData.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  )
}
