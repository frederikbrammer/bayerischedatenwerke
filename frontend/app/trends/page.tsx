"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { CarChart } from "@/components/charts/car-chart"
import { PartChart } from "@/components/charts/part-chart"
import { CaseStatusChart } from "@/components/charts/case-status-chart"
import { TopNavigation } from "@/components/top-navigation"
import { fetchTrendStats } from "@/lib/api"

export default function TrendsPage() {
  const [stats, setStats] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function loadStats() {
      setLoading(true)
      try {
        const data = await fetchTrendStats()
        if (data) {
          setStats(data)
        }
      } catch (error) {
        console.error("Error loading trend stats:", error)
      } finally {
        setLoading(false)
      }
    }

    loadStats()
  }, [])

  return (
    <>
      <TopNavigation />
      <div className="container mx-auto p-6">
        <h1 className="text-3xl font-bold mb-6">Litigation Trends</h1>

        {loading ? (
          <div className="text-center py-12">
            <p className="text-lg">Loading trend data...</p>
          </div>
        ) : stats ? (
          <Tabs defaultValue="overview" className="space-y-6">
            <TabsList>
              <TabsTrigger value="overview">Overview</TabsTrigger>
              <TabsTrigger value="cars">Cars</TabsTrigger>
              <TabsTrigger value="parts">Parts</TabsTrigger>
              <TabsTrigger value="outcomes">Outcomes</TabsTrigger>
            </TabsList>

            <TabsContent value="overview" className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle>Total Cases</CardTitle>
                    <CardDescription>All litigation cases</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="text-4xl font-bold">{stats.totalCases}</div>
                    <p className="text-xs text-muted-foreground">+12% from last year</p>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle>Won Cases</CardTitle>
                    <CardDescription>Successfully defended</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="text-4xl font-bold text-green-500">{stats.wonCases}</div>
                    <p className="text-xs text-muted-foreground">{stats.winRate}% success rate</p>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle>Lost Cases</CardTitle>
                    <CardDescription>Unsuccessful outcomes</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="text-4xl font-bold text-red-500">{stats.lostCases}</div>
                    <p className="text-xs text-muted-foreground">{stats.lossRate}% loss rate</p>
                  </CardContent>
                </Card>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Card>
                  <CardHeader>
                    <CardTitle>Case Outcomes</CardTitle>
                    <CardDescription>Distribution of case results</CardDescription>
                  </CardHeader>
                  <CardContent className="h-80">
                    <CaseStatusChart />
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle>Affected Cars</CardTitle>
                    <CardDescription>Distribution by car model</CardDescription>
                  </CardHeader>
                  <CardContent className="h-80">
                    <CarChart />
                  </CardContent>
                </Card>
              </div>

              <Card>
                <CardHeader>
                  <CardTitle>Affected Parts</CardTitle>
                  <CardDescription>Distribution by car part</CardDescription>
                </CardHeader>
                <CardContent className="h-80">
                  <PartChart />
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="cars">
              <Card>
                <CardHeader>
                  <CardTitle>Affected Cars</CardTitle>
                  <CardDescription>Detailed breakdown by car model</CardDescription>
                </CardHeader>
                <CardContent className="h-96">
                  <CarChart />
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="parts">
              <Card>
                <CardHeader>
                  <CardTitle>Affected Parts</CardTitle>
                  <CardDescription>Detailed breakdown by car part</CardDescription>
                </CardHeader>
                <CardContent className="h-96">
                  <PartChart />
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="outcomes">
              <Card>
                <CardHeader>
                  <CardTitle>Case Outcomes</CardTitle>
                  <CardDescription>Detailed breakdown of case results</CardDescription>
                </CardHeader>
                <CardContent className="h-96">
                  <CaseStatusChart />
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        ) : (
          <div className="text-center py-12">
            <p className="text-lg text-red-500">Failed to load trend data</p>
          </div>
        )}
      </div>
    </>
  )
}
