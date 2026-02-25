# Styleguide Scaffolding Templates

## Navigation Config — `/app/styleguide/navigation.ts`

```ts
export interface NavItem {
  name: string
  href: string
}

export interface NavSection {
  title: string
  items: NavItem[]
}

export const navigation: NavSection[] = [
  {
    title: "Foundation",
    items: [
      { name: "Design Tokens", href: "/styleguide" },
    ]
  },
  {
    title: "Components",
    items: [
      // Components will be added here by design-system:add-component
    ]
  }
]
```

## Layout with Sidebar — `/app/styleguide/layout.tsx`

```tsx
"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import { navigation } from "./navigation"

export default function StyleguideLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const pathname = usePathname()

  return (
    <div className="flex min-h-screen">
      {/* Sidebar - Fixed */}
      <aside className="w-64 border-r bg-card p-6 flex flex-col gap-6 fixed top-0 left-0 h-screen overflow-y-auto">
        <div>
          <Link href="/styleguide" className="text-xl font-bold">
            Design System
          </Link>
        </div>

        <nav className="flex flex-col gap-6">
          {navigation.map((section) => (
            <div key={section.title}>
              <h3 className="text-sm font-semibold text-muted-foreground mb-2">
                {section.title}
              </h3>
              <ul className="flex flex-col gap-1">
                {section.items.map((item) => (
                  <li key={item.href}>
                    <Link
                      href={item.href}
                      className={cn(
                        "block px-3 py-2 rounded-md text-sm transition-colors",
                        pathname === item.href
                          ? "bg-primary text-primary-foreground"
                          : "hover:bg-muted"
                      )}
                    >
                      {item.name}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </nav>
      </aside>

      {/* Main content - offset by sidebar width */}
      <main className="flex-1 ml-64 overflow-auto">
        {children}
      </main>
    </div>
  )
}
```

## Styleguide Page — `/app/styleguide/page.tsx`

The styleguide page should display ALL design tokens organized in sections:

### Required Sections

1. **Color Palette** — All CSS variable colors as swatches showing:
   - Variable name (e.g., `--primary`)
   - Resolved color value
   - Both light and dark values

2. **Primary Scale** — 50 through 900 shades in a horizontal strip

3. **Grey/Neutral Scale** — 50 through 900 shades

4. **Semantic Colors** — Success, warning, error/destructive, info with foreground pairs

5. **Typography** — Samples at each heading level (h1-h6) and body text sizes

6. **Border Radius** — Visual examples of `--radius` applied (sm, md, lg, full)

7. **Shadows** — Shadow samples (sm, md, lg)

8. **Component Demos** — Live examples of installed components:
   - Button (all variants: default, secondary, destructive, outline, ghost)
   - Card (with header, content, footer)
   - Badge (all variants)
   - Alert (default, destructive, with icon)
   - RadioGroup (basic group)

9. **Dark Mode Toggle** — Button to switch between light/dark themes for preview

### Implementation Notes

- Use CSS variable references directly (e.g., `bg-primary`, `text-muted-foreground`)
- Show the variable name alongside each swatch for developer reference
- Keep the page as a single scrollable view with anchor links
- Use the installed shadcn components — do not create custom components
