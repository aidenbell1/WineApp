import { z } from 'zod';

// Zod Schemas
export const saleSchema = z.object({
  id: z.string().uuid(),
  restaurant_id: z.string().uuid(),
  wine_id: z.string().uuid(),
  sale_date: z.string(), // Date string (YYYY-MM-DD)
  quantity: z.number().int().positive(),
  unit_price: z.number().positive(),
  total_amount: z.number().positive(),
  unit_cost: z.number().nonnegative().nullable(),
  server_name: z.string().max(100).nullable(),
  table_number: z.string().max(20).nullable(),
  notes: z.string().max(500).nullable(),
  created_at: z.string().datetime(),
  profit: z.number().nullable(),
  profit_margin: z.number().nullable(),
});

export const saleFormSchema = z.object({
  wine_id: z.string().uuid('Please select a wine'),
  sale_date: z.string().min(1, 'Sale date is required'),
  quantity: z.coerce.number().int().positive('Quantity must be at least 1'),
  unit_price: z.coerce.number().positive('Price must be greater than 0'),
  unit_cost: z.coerce.number().nonnegative().optional(),
  server_name: z.string().max(100).optional(),
  table_number: z.string().max(20).optional(),
  notes: z.string().max(500).optional(),
});

export const saleListResponseSchema = z.object({
  sales: z.array(saleSchema),
  total: z.number(),
  page: z.number(),
  page_size: z.number(),
  total_pages: z.number(),
});

// TypeScript Types
export type Sale = z.infer<typeof saleSchema>;
export type SaleFormData = z.infer<typeof saleFormSchema>;
export type SaleListResponse = z.infer<typeof saleListResponseSchema>;

export interface SaleListParams {
  restaurant_id: string;
  start_date?: string;
  end_date?: string;
  wine_id?: string;
  page?: number;
  page_size?: number;
}
