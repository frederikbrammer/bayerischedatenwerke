import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { AlertCircle } from "lucide-react"

interface ArgumentationSectionProps {
  offenseArgumentation: string
  defenseArgumentation: string
  suggestions: string[]
}

export function ArgumentationSection({
  offenseArgumentation,
  defenseArgumentation,
  suggestions,
}: ArgumentationSectionProps) {
  return (
    <div className="grid grid-cols-1 gap-6">
      <Card>
        <CardHeader>
          <CardTitle>Plaintiff's Argumentation</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm">{offenseArgumentation}</p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Our Defense</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm">{defenseArgumentation}</p>
        </CardContent>
      </Card>

      <Card className="border-blue-200 bg-blue-50 dark:bg-blue-950 dark:border-blue-800">
        <CardHeader className="pb-2">
          <CardTitle className="flex items-center gap-2 text-blue-800 dark:text-blue-300">
            <AlertCircle className="h-5 w-5" />
            Suggestions from Similar Cases
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="list-disc pl-5 space-y-2">
            {suggestions.map((suggestion, index) => (
              <li key={index} className="text-sm text-blue-800 dark:text-blue-300">
                {suggestion}
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>
    </div>
  )
}
