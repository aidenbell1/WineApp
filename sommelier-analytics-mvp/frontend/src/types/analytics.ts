import { z } from 'zod';

// Wine Sales Metric
export const wineSalesMetricSchema = z.object({
  wine_id: z.string().uuid(),
  wine_name: z.string(),
  producer: z.string().nullable(),
  vintage: z.number().nullable(),
  total_bottles_sold: z.number(),
  total_revenue: z.number(),
  total_profit: z.number().nullable(),
  avg_price: z.number(),
  profit_margin: z.number().nullable(),
  last_sale_date: z.string().nullable(),
  days_since_last_sale: z.number().nullable(),
});

export const topBottomWinesSchema = z.object({
  top_sellers: z.array(wineSalesMetricSchema),
  slow_movers: z.array(wineSalesMetricSchema),
});

// Sales Trend
export const salesTrendSchema = z.object({
  date: z.string(),
  total_sales: z.number(),
  total_revenue: z.number(),
  total_profit: z.number().nullable(),
  unique_wines_sold: z.number(),
});

export const salesTrendResponseSchema = z.object({
  period_start: z.string(),
  period_end: z.string(),
  trends: z.array(salesTrendSchema),
  total_sales: z.number(),
  total_revenue: z.number(),
  avg_daily_sales: z.number(),
});

// Inventory Health
export const inventoryHealthSchema = z.object({
  wine_id: z.string().uuid(),
  wine_name: z.string(),
  current_inventory: z.number(),
  avg_daily_sales: z.number(),
  days_until_stockout: z.number().nullable(),
  reorder_recommended: z.boolean(),
  overstocked: z.boolean(),
});

// Profit Analysis
export const profitAnalysisSchema = z.object({
  wine_id: z.string().uuid(),
  wine_name: z.string(),
  cost: z.number(),
  price: z.number(),
  profit_per_bottle: z.number(),
  profit_margin: z.number(),
  markup_percentage: z.number(),
  total_profit_ytd: z.number(),
  recommended_price: z.number().nullable(),
});

// Dashboard Summary
export const dashboardSummarySchema = z.object({
  total_wines: z.number(),
  total_bottles_in_stock: z.number(),
  total_sales_last_30_days: z.number(),
  revenue_last_30_days: z.number(),
  profit_last_30_days: z.number().nullable(),
  avg_profit_margin: z.number().nullable(),
  top_wine_this_month: z.string().nullable(),
  slowest_wine: z.string().nullable(),
  wines_needing_reorder: z.number(),
  overstocked_wines: z.number(),
});

// TypeScript Types
export type WineSalesMetric = z.infer<typeof wineSalesMetricSchema>;
export type TopBottomWines = z.infer<typeof topBottomWinesSchema>;
export type SalesTrend = z.infer<typeof salesTrendSchema>;
export type SalesTrendResponse = z.infer<typeof salesTrendResponseSchema>;
export type InventoryHealth = z.infer<typeof inventoryHealthSchema>;
export type ProfitAnalysis = z.infer<typeof profitAnalysisSchema>;
export type DashboardSummary = z.infer<typeof dashboardSummarySchema>;
