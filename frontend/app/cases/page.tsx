"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { CaseTable } from "@/components/case-table"
import { Plus, Search } from "lucide-react"
import Link from "next/link"
import { TopNavigation } from "@/components/top-navigation"

export default function CasesPage() {
  const [searchQuery, setSearchQuery] = useState("")

  return (
    <>
      <TopNavigation />
      <div className="container mx-auto p-6">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold">Cases</h1>
          <Button asChild>
            <Link href="/cases/new">
              <Plus className="mr-2 h-4 w-4" /> New Case
            </Link>
          </Button>
        </div>

        <div className="relative mb-6">
          <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            type="search"
            placeholder="Search cases"
            className="pl-8"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>

        <CaseTable searchQuery={searchQuery} />
      </div>
    </>
  )
}
