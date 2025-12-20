import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { toast } from 'sonner';
import type { Sale, SaleFormData, SaleListResponse, SaleListParams } from '@/types';

export function useSales(params: SaleListParams) {
  return useQuery<SaleListResponse>({
    queryKey: ['sales', params],
    queryFn: () => api.getSales(params),
    enabled: !!params.restaurant_id,
  });
}

export function useSale(id: string) {
  return useQuery<Sale>({
    queryKey: ['sale', id],
    queryFn: () => api.getSale(id),
    enabled: !!id,
  });
}

export function useCreateSale(restaurantId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: SaleFormData) =>
      api.createSale({ ...data, restaurant_id: restaurantId }),
    
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sales'] });
      queryClient.invalidateQueries({ queryKey: ['wines'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
      queryClient.invalidateQueries({ queryKey: ['sales-trends'] });
      queryClient.invalidateQueries({ queryKey: ['top-bottom-wines'] });
      toast.success('Sale recorded successfully');
    },
    
    onError: (error: Error) => {
      toast.error(error.message || 'Failed to record sale');
    },
  });
}

export function useDeleteSale() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: string) => api.deleteSale(id),
    
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sales'] });
      queryClient.invalidateQueries({ queryKey: ['wines'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
      queryClient.invalidateQueries({ queryKey: ['sales-trends'] });
      queryClient.invalidateQueries({ queryKey: ['top-bottom-wines'] });
      toast.success('Sale deleted successfully');
    },
    
    onError: (error: Error) => {
      toast.error(error.message || 'Failed to delete sale');
    },
  });
}

export function useBulkUploadSales(restaurantId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (file: File) => api.bulkUploadSales(restaurantId, file),
    
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['sales'] });
      queryClient.invalidateQueries({ queryKey: ['wines'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
      queryClient.invalidateQueries({ queryKey: ['sales-trends'] });
      queryClient.invalidateQueries({ queryKey: ['top-bottom-wines'] });
      toast.success(`Successfully uploaded ${data.sales_created} sales`);
      
      if (data.errors && data.errors.length > 0) {
        toast.warning(`${data.errors.length} rows had errors`);
      }
    },
    
    onError: (error: Error) => {
      toast.error(error.message || 'Failed to upload sales');
    },
  });
}
