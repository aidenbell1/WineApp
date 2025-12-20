# Sommelier Analytics - Frontend

Modern Next.js 14 dashboard for wine sales analytics.

## 🎯 What's Built

- ✅ Next.js 14 with App Router
- ✅ TypeScript with Zod validation
- ✅ TanStack Query (React Query) for state management
- ✅ Tailwind CSS + shadcn/ui components
- ✅ Type-safe API client
- ✅ Custom hooks for all API endpoints
- ✅ Toast notifications (Sonner)
- ✅ Recharts for data visualization

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ installed
- Backend API running on http://localhost:8000
- Restaurant ID from backend

### Installation

```bash
# 1. Install dependencies
npm install

# 2. Install shadcn/ui
npx shadcn-ui@latest init

# 3. Install required components
npx shadcn-ui@latest add card table input label select dialog badge tabs separator skeleton

# 4. Set up environment
cp .env.local.example .env.local
```

Edit `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_DEMO_RESTAURANT_ID=your-restaurant-id-here
```

### Run Development Server

```bash
npm run dev
```

Open http://localhost:3000

## 📁 Project Structure

```
src/
├── app/                    # Next.js App Router
│   ├── layout.tsx         # Root layout with providers
│   ├── page.tsx           # Landing page
│   ├── globals.css        # Global styles
│   └── (dashboard)/       # Dashboard routes
│
├── components/
│   ├── ui/               # shadcn/ui components
│   ├── layout/           # Layout components
│   ├── charts/           # Chart components
│   ├── tables/           # Table components
│   ├── forms/            # Form components
│   ├── cards/            # Card components
│   └── providers/        # Context providers
│
├── lib/
│   ├── api.ts           # Type-safe API client
│   ├── utils.ts         # Utility functions
│   ├── queryClient.ts   # React Query config
│   └── constants.ts     # App constants
│
├── hooks/
│   ├── useAnalytics.ts  # Analytics hooks
│   ├── useWines.ts      # Wine CRUD hooks
│   └── useSales.ts      # Sales CRUD hooks
│
└── types/
    ├── wine.ts          # Wine types + schemas
    ├── sale.ts          # Sale types + schemas
    ├── analytics.ts     # Analytics types
    └── restaurant.ts    # Restaurant types
```

## 🔧 Key Features

### Type-Safe API Client

```typescript
import { api } from '@/lib/api';

// All methods are type-safe with Zod validation
const wines = await api.getWines({ restaurant_id: id });
const summary = await api.getDashboardSummary(id);
```

### React Query Hooks

```typescript
import { useWines, useCreateWine } from '@/hooks/useWines';

function WinesPage() {
  const { data, isLoading } = useWines({ restaurant_id });
  const createWine = useCreateWine(restaurant_id);
  
  // Automatic cache invalidation, optimistic updates, etc.
}
```

### Form Validation with Zod

```typescript
import { wineFormSchema } from '@/types/wine';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

const form = useForm({
  resolver: zodResolver(wineFormSchema),
});
```

## 📊 Pages to Build

### ✅ Already Created
- Landing page (`/`)
- Root layout with providers

### 🚧 To Build

**Dashboard** (`/dashboard`)
- Summary metrics cards
- Sales trend chart
- Top/bottom wines
- Inventory alerts

**Wines** (`/wines`)
- Wine list table (searchable, filterable, paginated)
- Add wine form
- Edit wine form
- CSV upload

**Sales** (`/sales`)
- Sales history table
- Add sale form
- CSV upload

**Analytics** (`/analytics`)
- Deep dive into analytics
- Multiple chart views
- Export data

**Inventory** (`/inventory`)
- Stock levels
- Reorder alerts
- Low stock warnings

## 🎨 Component Examples

### StatCard

```typescript
<StatCard
  title="Total Wines"
  value={data.total_wines}
  icon={<Wine className="h-4 w-4" />}
/>
```

### SalesChart

```typescript
<SalesChart restaurantId={restaurantId} />
```

### WineTable

```typescript
<WineTable
  wines={data.wines}
  onEdit={handleEdit}
  onDelete={handleDelete}
/>
```

## 🎯 Development Workflow

### 1. Create a Component

```typescript
// src/components/cards/StatCard.tsx
import { Card } from '@/components/ui/card';

export function StatCard({ title, value }) {
  return (
    <Card>
      <h3>{title}</h3>
      <p>{value}</p>
    </Card>
  );
}
```

### 2. Use React Query Hook

```typescript
'use client';

import { useDashboardSummary } from '@/hooks/useAnalytics';

export function DashboardPage() {
  const { data, isLoading } = useDashboardSummary(restaurantId);
  
  if (isLoading) return <LoadingSkeleton />;
  
  return <div>{/* Use data */}</div>;
}
```

### 3. Handle Mutations

```typescript
import { useCreateWine } from '@/hooks/useWines';

export function AddWineForm() {
  const createWine = useCreateWine(restaurantId);
  
  const onSubmit = (data) => {
    createWine.mutate(data, {
      onSuccess: () => {
        // Toast notification handled automatically
        // Cache invalidated automatically
      }
    });
  };
}
```

## 🎨 Styling

### Tailwind CSS

```tsx
<div className="flex items-center gap-4 p-6 rounded-lg bg-white shadow">
```

### shadcn/ui Components

```tsx
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';

<Card>
  <Button variant="default">Click me</Button>
</Card>
```

### Custom Utilities

```typescript
import { formatCurrency, formatDate } from '@/lib/utils';

formatCurrency(99.99) // "$99.99"
formatDate('2025-01-08', 'MMM d, yyyy') // "Jan 8, 2025"
```

## 🚀 Deployment

### Vercel (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Environment Variables in Vercel

Add these in Vercel dashboard:
```
NEXT_PUBLIC_API_URL=https://your-api.com
NEXT_PUBLIC_DEMO_RESTAURANT_ID=<id>
```

### Other Platforms

- **Netlify**: Works out of the box
- **Railway**: Add `next build` and `next start`
- **AWS Amplify**: Connect GitHub repo

## 📚 Learning Resources

**Next.js 14**
- [App Router Docs](https://nextjs.org/docs/app)
- [Server Components](https://nextjs.org/docs/app/building-your-application/rendering/server-components)

**TanStack Query**
- [Quick Start](https://tanstack.com/query/latest/docs/framework/react/quick-start)
- [Mutations](https://tanstack.com/query/latest/docs/framework/react/guides/mutations)

**shadcn/ui**
- [Component Docs](https://ui.shadcn.com/docs/components)
- [Installation](https://ui.shadcn.com/docs/installation/next)

**Recharts**
- [Examples](https://recharts.org/en-US/examples)
- [API Reference](https://recharts.org/en-US/api)

## 🐛 Troubleshooting

### "Module not found" errors
```bash
npm install
rm -rf .next
npm run dev
```

### TypeScript errors
```bash
npm run type-check
```

### API not connecting
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Verify backend is running on port 8000
- Check browser console for CORS errors

### React Query not working
- Ensure `QueryProvider` wraps your app in `layout.tsx`
- Check React Query DevTools in browser

## ✅ Checklist

### Setup
- [ ] Install dependencies (`npm install`)
- [ ] Install shadcn/ui (`npx shadcn-ui@latest init`)
- [ ] Add required components
- [ ] Set up `.env.local`
- [ ] Get restaurant ID from backend
- [ ] Test connection to backend

### Components to Build
- [ ] Sidebar navigation
- [ ] Navbar
- [ ] StatCard
- [ ] SalesChart
- [ ] WineTable
- [ ] SalesTable
- [ ] WineForm
- [ ] CSVUploadForm

### Pages to Build
- [ ] Dashboard page
- [ ] Wines list page
- [ ] Add wine page
- [ ] Sales list page
- [ ] Analytics page

### Final Polish
- [ ] Loading states
- [ ] Error handling
- [ ] Mobile responsive
- [ ] Dark mode (optional)
- [ ] Deploy to Vercel

## 📞 Need Help?

- **API Client**: See `src/lib/api.ts`
- **Hooks**: See `src/hooks/`
- **Types**: See `src/types/`
- **Examples**: See `FRONTEND_SETUP.md`

---

**Ready to build!** 🎨

The foundation is solid. Just add UI components and pages. Use shadcn/ui for components, React Query hooks for data, and you're set!
