"use client"

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts"

// Mock data for case status
const statusData = [
  { name: "2020", won: 15, lost: 8, inProgress: 2 },
  { name: "2021", won: 18, lost: 7, inProgress: 3 },
  { name: "2022", won: 22, lost: 9, inProgress: 4 },
  { name: "2023", won: 23, lost: 8, inProgress: 6 },
  { name: "2024", won: 0, lost: 0, inProgress: 17 },
]

export function CaseStatusChart() {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart
        data={statusData}
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
        <Bar dataKey="won" fill="#22c55e" name="Won" />
        <Bar dataKey="lost" fill="#ef4444" name="Lost" />
        <Bar dataKey="inProgress" fill="#3b82f6" name="In Progress" />
      </BarChart>
    </ResponsiveContainer>
  )
}
