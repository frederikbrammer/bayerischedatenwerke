"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"

export function TopNavigation() {
  const pathname = usePathname()

  const isActive = (path: string) => {
    return pathname === path || pathname.startsWith(`${path}/`)
  }

  return (
    <div className="border-b">
      <div className="container mx-auto px-6">
        <div className="flex items-center justify-between h-16">
          <h1 className="text-xl font-bold">BayerscheDatenWerke</h1>

          <nav className="absolute left-1/2 transform -translate-x-1/2 flex space-x-4">
            <Link
              href="/cases"
              className={cn(
                "px-4 py-2 rounded-full text-sm font-medium transition-colors",
                isActive("/cases")
                  ? "text-blue-600 bg-blue-100/80"
                  : "text-muted-foreground hover:text-foreground hover:bg-muted/50",
              )}
            >
              Cases
            </Link>
            <Link
              href="/trends"
              className={cn(
                "px-4 py-2 rounded-full text-sm font-medium transition-colors",
                isActive("/trends")
                  ? "text-blue-600 bg-blue-100/80"
                  : "text-muted-foreground hover:text-foreground hover:bg-muted/50",
              )}
            >
              Trends
            </Link>
          </nav>
        </div>
      </div>
    </div>
  )
}
