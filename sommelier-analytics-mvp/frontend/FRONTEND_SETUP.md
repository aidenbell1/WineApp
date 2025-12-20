# Frontend Setup Guide

## What's Been Created

✅ **Project Structure**
- package.json with all dependencies
- TypeScript configuration
- Tailwind CSS setup
- Next.js 14 App Router configuration

✅ **Type System**
- Complete Zod schemas for validation
- TypeScript types for all entities
- Wine, Sale, Analytics, Restaurant types

✅ **API Layer**
- Enhanced API client with Zod validation
- Error handling
- Type-safe methods for all endpoints

✅ **React Query Integration**
- Query client configuration
- Custom hooks (useAnalytics, useWines, useSales)
- Optimistic updates
- Cache management

✅ **Utilities**
- Formatting functions (currency, dates, percentages)
- Helper functions
- Constants

✅ **Providers**
- React Query Provider
- Toast notifications (Sonner)

✅ **Initial Pages**
- Landing page
- Root layout with providers

## Installation Steps

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Install Additional Dependencies

Some packages need to be added:

```bash
npm install tailwindcss-animate
npm install postcss autoprefixer
npx shadcn-ui@latest init
```

When prompted by shadcn-ui:
- Would you like to use TypeScript? **Yes**
- Which style would you like to use? **Default**
- Which color would you like to use as base color? **Slate**
- Where is your global CSS file? **src/app/globals.css**
- Would you like to use CSS variables for colors? **Yes**
- Where is your tailwind.config.js located? **tailwind.config.ts**
- Configure the import alias for components? **@/components**
- Configure the import alias for utils? **@/lib/utils**

### 3. Install shadcn/ui Components

```bash
# Core components needed
npx shadcn-ui@latest add card
npx shadcn-ui@latest add table
npx shadcn-ui@latest add input
npx shadcn-ui@latest add label
npx shadcn-ui@latest add select
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add badge
npx shadcn-ui@latest add tabs
npx shadcn-ui@latest add separator
npx shadcn-ui@latest add skeleton
```

### 4. Create Environment File

```bash
cp .env.local.example .env.local
```

Edit `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_DEMO_RESTAURANT_ID=your-restaurant-id-from-backend
```

### 5. Create Missing Component Files

You need to create these component files manually or using shadcn-ui CLI:

**Layout Components** (create these):
- `src/components/layout/Sidebar.tsx`
- `src/components/layout/Navbar.tsx`

**Chart Components** (create these):
- `src/components/charts/SalesChart.tsx`
- `src/components/charts/TopWinesChart.tsx`

**Card Components** (create these):
- `src/components/cards/StatCard.tsx`

**Form Components** (create these):
- `src/components/forms/WineForm.tsx`
- `src/components/forms/CSVUploadForm.tsx`

**Table Components** (create these):
- `src/components/tables/WineTable.tsx`
- `src/components/tables/SalesTable.tsx`

### 6. Create Dashboard Pages

Create these page files:

**Dashboard Layout**:
```tsx
// src/app/(dashboard)/layout.tsx
import { Sidebar } from "@/components/layout/Sidebar";
import { Navbar } from "@/components/layout/Navbar";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex h-screen">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <Navbar />
        <main className="flex-1 overflow-auto p-6">
          {children}
        </main>
      </div>
    </div>
  );
}
```

**Dashboard Page**:
```tsx
// src/app/(dashboard)/dashboard/page.tsx
'use client';

import { useDashboardSummary } from "@/hooks/useAnalytics";
import { StatCard } from "@/components/cards/StatCard";

export default function DashboardPage() {
  const restaurantId = process.env.NEXT_PUBLIC_DEMO_RESTAURANT_ID!;
  const { data, isLoading } = useDashboardSummary(restaurantId);

  if (isLoading) return <div>Loading...</div>;

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Total Wines"
          value={data?.total_wines || 0}
        />
        <StatCard
          title="Bottles in Stock"
          value={data?.total_bottles_in_stock || 0}
        />
        <StatCard
          title="Sales (30d)"
          value={data?.total_sales_last_30_days || 0}
        />
        <StatCard
          title="Revenue (30d)"
          value={`$${data?.revenue_last_30_days.toFixed(2)}`}
        />
      </div>
    </div>
  );
}
```

## Component Templates

### StatCard Component

```tsx
// src/components/cards/StatCard.tsx
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface StatCardProps {
  title: string;
  value: string | number;
  description?: string;
  icon?: React.ReactNode;
}

export function StatCard({ title, value, description, icon }: StatCardProps) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        {icon}
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        {description && (
          <p className="text-xs text-muted-foreground">{description}</p>
        )}
      </CardContent>
    </Card>
  );
}
```

### Sidebar Component

```tsx
// src/components/layout/Sidebar.tsx
'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Wine, BarChart3, Package, ShoppingCart, Settings } from 'lucide-react';
import { cn } from '@/lib/utils';

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: BarChart3 },
  { name: 'Wines', href: '/wines', icon: Wine },
  { name: 'Sales', href: '/sales', icon: ShoppingCart },
  { name: 'Analytics', href: '/analytics', icon: BarChart3 },
  { name: 'Inventory', href: '/inventory', icon: Package },
  { name: 'Settings', href: '/settings', icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <div className="w-64 bg-gray-900 text-white">
      <div className="p-6">
        <div className="flex items-center gap-2">
          <Wine className="h-8 w-8" />
          <span className="text-xl font-bold">Sommelier</span>
        </div>
      </div>

      <nav className="space-y-1 px-3">
        {navigation.map((item) => {
          const isActive = pathname === item.href;
          const Icon = item.icon;
          
          return (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                'flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition',
                isActive
                  ? 'bg-gray-800 text-white'
                  : 'text-gray-300 hover:bg-gray-800 hover:text-white'
              )}
            >
              <Icon className="h-5 w-5" />
              {item.name}
            </Link>
          );
        })}
      </nav>
    </div>
  );
}
```

### Sales Chart Component

```tsx
// src/components/charts/SalesChart.tsx
'use client';

import { useSalesTrends } from '@/hooks/useAnalytics';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { formatCurrency, formatDate } from '@/lib/utils';

export function SalesChart({ restaurantId }: { restaurantId: string }) {
  const { data, isLoading } = useSalesTrends(restaurantId);

  if (isLoading) return <div>Loading chart...</div>;

  const chartData = data?.trends.map(trend => ({
    date: formatDate(trend.date, 'MMM d'),
    revenue: parseFloat(trend.total_revenue.toString()),
  })) || [];

  return (
    <Card>
      <CardHeader>
        <CardTitle>Sales Trend</CardTitle>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis tickFormatter={(value) => `$${value}`} />
            <Tooltip
              formatter={(value) => formatCurrency(value as number)}
            />
            <Line
              type="monotone"
              dataKey="revenue"
              stroke="#3b82f6"
              strokeWidth={2}
            />
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
```

## Development Workflow

### 1. Start the Development Server

```bash
npm run dev
```

Open http://localhost:3000

### 2. Connect to Backend

Make sure your backend is running on http://localhost:8000

### 3. Get Restaurant ID

1. Go to http://localhost:8000/docs
2. Create a restaurant
3. Copy the restaurant ID
4. Add it to `.env.local`:
   ```
   NEXT_PUBLIC_DEMO_RESTAURANT_ID=<paste-id-here>
   ```
5. Restart the Next.js dev server

### 4. Test the Dashboard

Navigate to http://localhost:3000/dashboard

You should see:
- Navigation sidebar
- Dashboard metrics
- (Add wines and sales via backend first to see data)

## Build Priority

### Week 1 (Foundation)
1. ✅ Install all dependencies
2. ✅ Set up environment variables
3. ✅ Create layout components (Sidebar, Navbar)
4. ✅ Create dashboard page with stat cards
5. ✅ Test connection to backend API

### Week 2 (Core Features)
1. Create WineTable component
2. Create wines list page (`/wines`)
3. Create WineForm component
4. Create add wine page (`/wines/new`)
5. Create CSV upload form
6. Test CRUD operations

### Week 3 (Analytics & Charts)
1. Create SalesChart component (Recharts)
2. Create TopWinesChart
3. Create analytics page
4. Create inventory health page
5. Polish UI/UX

### Week 4 (Polish & Deploy)
1. Add loading states (Skeleton)
2. Error boundaries
3. Mobile responsive design
4. Deploy to Vercel

## Tips

1. **Use shadcn-ui CLI**: Instead of manually creating components, use `npx shadcn-ui@latest add <component>`

2. **React Query DevTools**: Open http://localhost:3000 and look for the React Query icon in the bottom corner

3. **Hot Reload**: Changes to files automatically reload the page

4. **Type Safety**: If you see TypeScript errors, run `npm run type-check`

5. **API Errors**: Check the Network tab in browser DevTools

## Next Steps

1. Complete the missing component files listed above
2. Create the wines list page
3. Add data tables for wines and sales
4. Implement CSV upload
5. Add charts to analytics page
6. Make it mobile responsive

All the heavy lifting is done - you have:
- ✅ Type-safe API client
- ✅ React Query hooks
- ✅ Proper state management
- ✅ Error handling
- ✅ Toast notifications

Just build the UI components and pages!
