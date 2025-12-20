import { z } from 'zod';

// Wine Type Enums
export const WineType = {
  RED: 'red',
  WHITE: 'white',
  ROSE: 'rose',
  SPARKLING: 'sparkling',
  DESSERT: 'dessert',
  FORTIFIED: 'fortified',
} as const;

export const WineBody = {
  LIGHT: 'light',
  MEDIUM: 'medium',
  FULL: 'full',
} as const;

// Zod Schemas
export const wineSchema = z.object({
  id: z.string().uuid(),
  restaurant_id: z.string().uuid(),
  name: z.string().min(1).max(255),
  producer: z.string().max(255).nullable(),
  vintage: z.number().int().min(1900).max(2030).nullable(),
  varietal: z.string().max(100).nullable(),
  region: z.string().max(255).nullable(),
  country: z.string().max(100).nullable(),
  wine_type: z.enum(['red', 'white', 'rose', 'sparkling', 'dessert', 'fortified']).nullable(),
  body: z.enum(['light', 'medium', 'full']).nullable(),
  sweetness: z.number().int().min(1).max(5).nullable(),
  acidity: z.number().int().min(1).max(5).nullable(),
  tannin: z.number().int().min(1).max(5).nullable(),
  alcohol_content: z.number().min(0).max(20).nullable(),
  price: z.number().positive(),
  cost: z.number().nonnegative().nullable(),
  inventory_count: z.number().int().nonnegative(),
  tasting_notes: z.string().nullable(),
  bottle_size: z.string().default('750ml'),
  sku: z.string().max(100).nullable(),
  times_sold: z.number().int().nonnegative(),
  created_at: z.string().datetime(),
  updated_at: z.string().datetime(),
  profit_margin: z.number().nullable(),
  markup: z.number().nullable(),
});

export const wineFormSchema = z.object({
  name: z.string().min(1, 'Wine name is required').max(255),
  producer: z.string().max(255).optional(),
  vintage: z.coerce.number().int().min(1900).max(2030).optional(),
  varietal: z.string().max(100).optional(),
  region: z.string().max(255).optional(),
  country: z.string().max(100).optional(),
  wine_type: z.enum(['red', 'white', 'rose', 'sparkling', 'dessert', 'fortified']).optional(),
  body: z.enum(['light', 'medium', 'full']).optional(),
  sweetness: z.coerce.number().int().min(1).max(5).optional(),
  acidity: z.coerce.number().int().min(1).max(5).optional(),
  tannin: z.coerce.number().int().min(1).max(5).optional(),
  alcohol_content: z.coerce.number().min(0).max(20).optional(),
  price: z.coerce.number().positive('Price must be greater than 0'),
  cost: z.coerce.number().nonnegative().optional(),
  inventory_count: z.coerce.number().int().nonnegative().default(0),
  tasting_notes: z.string().optional(),
  bottle_size: z.string().default('750ml'),
  sku: z.string().max(100).optional(),
});

export const wineListResponseSchema = z.object({
  wines: z.array(wineSchema),
  total: z.number(),
  page: z.number(),
  page_size: z.number(),
  total_pages: z.number(),
});

// TypeScript Types
export type Wine = z.infer<typeof wineSchema>;
export type WineFormData = z.infer<typeof wineFormSchema>;
export type WineListResponse = z.infer<typeof wineListResponseSchema>;

export interface WineListParams {
  restaurant_id: string;
  page?: number;
  page_size?: number;
  search?: string;
  wine_type?: string;
}
