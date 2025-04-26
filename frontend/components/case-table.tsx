"use client"
import { useRouter } from "next/navigation"
import { useState } from "react"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { ArrowDown, ArrowUp } from "lucide-react"

// Mock data for cases
const mockCases = [
  {
    id: "1",
    title: "Smith v. Bayersche Motors",
    status: "won",
    jurisdiction: "California",
    caseType: "Liability",
    date: "2023-05-15",
  },
  {
    id: "2",
    title: "Johnson Family Trust v. Bayersche",
    status: "lost",
    jurisdiction: "New York",
    caseType: "Liability",
    date: "2023-08-22",
  },
  {
    id: "3",
    title: "Martinez Product Liability Claim",
    status: "in progress",
    jurisdiction: "Texas",
    caseType: "Liability",
    date: "2024-01-10",
  },
  {
    id: "4",
    title: "Williams Class Action",
    status: "in progress",
    jurisdiction: "Florida",
    caseType: "Liability",
    date: "2024-02-28",
  },
  {
    id: "5",
    title: "Garcia v. Bayersche Manufacturing",
    status: "won",
    jurisdiction: "Michigan",
    caseType: "Liability",
    date: "2023-11-05",
  },
]

type CaseStatus = "won" | "lost" | "in progress"
type SortField = "title" | "status" | "jurisdiction" | "caseType" | "date"
type SortDirection = "asc" | "desc"

interface CaseTableProps {
  searchQuery: string
}

export function CaseTable({ searchQuery }: CaseTableProps) {
  const router = useRouter()
  const [sortField, setSortField] = useState<SortField>("date")
  const [sortDirection, setSortDirection] = useState<SortDirection>("desc")

  // Filter cases based on search query (mock semantic search)
  const filteredCases = mockCases.filter(
    (caseItem) =>
      caseItem.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      caseItem.jurisdiction.toLowerCase().includes(searchQuery.toLowerCase()),
  )

  // Sort cases based on sort field and direction
  const sortedCases = [...filteredCases].sort((a, b) => {
    if (sortField === "status") {
      // Custom sort order for status: "in progress" > "won" > "lost"
      const statusOrder = { "in progress": 0, won: 1, lost: 2 }
      const aValue = statusOrder[a.status as keyof typeof statusOrder]
      const bValue = statusOrder[b.status as keyof typeof statusOrder]
      return sortDirection === "asc" ? aValue - bValue : bValue - aValue
    }

    if (sortField === "date") {
      const aDate = new Date(a.date).getTime()
      const bDate = new Date(b.date).getTime()
      return sortDirection === "asc" ? aDate - bDate : bDate - aDate
    }

    const aValue = a[sortField]
    const bValue = b[sortField]

    if (aValue < bValue) return sortDirection === "asc" ? -1 : 1
    if (aValue > bValue) return sortDirection === "asc" ? 1 : -1
    return 0
  })

  const getStatusColor = (status: CaseStatus) => {
    switch (status) {
      case "won":
        return "bg-green-500 hover:bg-green-600"
      case "lost":
        return "bg-red-500 hover:bg-red-600"
      case "in progress":
        return "bg-blue-500 hover:bg-blue-600"
      default:
        return ""
    }
  }

  const handleRowClick = (id: string) => {
    router.push(`/cases/${id}`)
  }

  const handleSort = (field: SortField) => {
    if (sortField === field) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc")
    } else {
      setSortField(field)
      setSortDirection("asc")
    }
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    })
  }

  const SortIcon = ({ field }: { field: SortField }) => {
    if (sortField !== field) return null
    return sortDirection === "asc" ? (
      <ArrowUp className="ml-1 h-4 w-4 inline" />
    ) : (
      <ArrowDown className="ml-1 h-4 w-4 inline" />
    )
  }

  return (
    <div className="border rounded-md">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>
              <Button variant="ghost" className="p-0 font-medium" onClick={() => handleSort("title")}>
                Title <SortIcon field="title" />
              </Button>
            </TableHead>
            <TableHead>
              <Button variant="ghost" className="p-0 font-medium" onClick={() => handleSort("status")}>
                Status <SortIcon field="status" />
              </Button>
            </TableHead>
            <TableHead>
              <Button variant="ghost" className="p-0 font-medium" onClick={() => handleSort("jurisdiction")}>
                Jurisdiction <SortIcon field="jurisdiction" />
              </Button>
            </TableHead>
            <TableHead>
              <Button variant="ghost" className="p-0 font-medium" onClick={() => handleSort("caseType")}>
                Case Type <SortIcon field="caseType" />
              </Button>
            </TableHead>
            <TableHead>
              <Button variant="ghost" className="p-0 font-medium" onClick={() => handleSort("date")}>
                Date <SortIcon field="date" />
              </Button>
            </TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {sortedCases.length > 0 ? (
            sortedCases.map((caseItem) => (
              <TableRow
                key={caseItem.id}
                className="cursor-pointer hover:bg-muted/50"
                onClick={() => handleRowClick(caseItem.id)}
              >
                <TableCell className="font-medium">{caseItem.title}</TableCell>
                <TableCell>
                  <Badge className={getStatusColor(caseItem.status as CaseStatus)}>
                    {caseItem.status.charAt(0).toUpperCase() + caseItem.status.slice(1)}
                  </Badge>
                </TableCell>
                <TableCell>{caseItem.jurisdiction}</TableCell>
                <TableCell>{caseItem.caseType}</TableCell>
                <TableCell>{formatDate(caseItem.date)}</TableCell>
              </TableRow>
            ))
          ) : (
            <TableRow>
              <TableCell colSpan={5} className="text-center py-6 text-muted-foreground">
                No cases found matching your search.
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </div>
  )
}
