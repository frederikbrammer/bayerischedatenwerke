"use client"

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts"

// Mock data for car models affected
const carData = [
  { name: "Model S", count: 42, won: 28, lost: 9, inProgress: 5 },
  { name: "Model X", count: 35, won: 20, lost: 10, inProgress: 5 },
  { name: "Model Y", count: 28, won: 18, lost: 6, inProgress: 4 },
  { name: "Model Z", count: 22, won: 12, lost: 7, inProgress: 3 },
]

export function CarChart() {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart
        data={carData}
        margin={{
          top: 20,
          right: 30,
          left: 20,
          bottom: 5,
        }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="won" stackId="a" fill="#22c55e" name="Won" />
        <Bar dataKey="lost" stackId="a" fill="#ef4444" name="Lost" />
        <Bar dataKey="inProgress" stackId="a" fill="#3b82f6" name="In Progress" />
      </BarChart>
    </ResponsiveContainer>
  )
}
