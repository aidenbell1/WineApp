import { z } from 'zod';

export const restaurantSchema = z.object({
  id: z.string().uuid(),
  name: z.string(),
  email: z.string().email(),
  phone: z.string().nullable(),
  address: z.string().nullable(),
  city: z.string().nullable(),
  state: z.string().nullable(),
  zip_code: z.string().nullable(),
  is_active: z.boolean(),
  subscription_tier: z.string(),
});

export const restaurantFormSchema = z.object({
  name: z.string().min(1, 'Restaurant name is required'),
  email: z.string().email('Valid email is required'),
  phone: z.string().optional(),
  address: z.string().optional(),
  city: z.string().optional(),
  state: z.string().optional(),
  zip_code: z.string().optional(),
});

export type Restaurant = z.infer<typeof restaurantSchema>;
export type RestaurantFormData = z.infer<typeof restaurantFormSchema>;
