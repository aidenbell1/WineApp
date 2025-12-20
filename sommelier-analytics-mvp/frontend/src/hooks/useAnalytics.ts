import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api';
import type {
  DashboardSummary,
  TopBottomWines,
  SalesTrendResponse,
  InventoryHealth,
  ProfitAnalysis,
} from '@/types';

export function useDashboardSummary(restaurantId: string) {
  return useQuery<DashboardSummary>({
    queryKey: ['dashboard', restaurantId],
    queryFn: () => api.getDashboardSummary(restaurantId),
    enabled: !!restaurantId,
  });
}

export function useTopBottomWines(
  restaurantId: string,
  params?: { start_date?: string; end_date?: string; limit?: number }
) {
  return useQuery<TopBottomWines>({
    queryKey: ['top-bottom-wines', restaurantId, params],
    queryFn: () => api.getTopBottomWines(restaurantId, params),
    enabled: !!restaurantId,
  });
}

export function useSalesTrends(
  restaurantId: string,
  params?: { start_date?: string; end_date?: string }
) {
  return useQuery<SalesTrendResponse>({
    queryKey: ['sales-trends', restaurantId, params],
    queryFn: () => api.getSalesTrends(restaurantId, params),
    enabled: !!restaurantId,
  });
}

export function useInventoryHealth(restaurantId: string) {
  return useQuery<InventoryHealth[]>({
    queryKey: ['inventory-health', restaurantId],
    queryFn: () => api.getInventoryHealth(restaurantId),
    enabled: !!restaurantId,
  });
}

export function useProfitAnalysis(restaurantId: string) {
  return useQuery<ProfitAnalysis[]>({
    queryKey: ['profit-analysis', restaurantId],
    queryFn: () => api.getProfitAnalysis(restaurantId),
    enabled: !!restaurantId,
  });
}
