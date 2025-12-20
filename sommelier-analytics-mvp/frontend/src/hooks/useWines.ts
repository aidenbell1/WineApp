import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { toast } from 'sonner';
import type { Wine, WineFormData, WineListResponse, WineListParams } from '@/types';

export function useWines(params: WineListParams) {
  return useQuery<WineListResponse>({
    queryKey: ['wines', params],
    queryFn: () => api.getWines(params),
    enabled: !!params.restaurant_id,
  });
}

export function useWine(id: string) {
  return useQuery<Wine>({
    queryKey: ['wine', id],
    queryFn: () => api.getWine(id),
    enabled: !!id,
  });
}

export function useCreateWine(restaurantId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: WineFormData) =>
      api.createWine({ ...data, restaurant_id: restaurantId }),
    
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['wines'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
      toast.success('Wine created successfully');
    },
    
    onError: (error: Error) => {
      toast.error(error.message || 'Failed to create wine');
    },
  });
}

export function useUpdateWine() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<WineFormData> }) =>
      api.updateWine(id, data),
    
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['wines'] });
      queryClient.invalidateQueries({ queryKey: ['wine', variables.id] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
      toast.success('Wine updated successfully');
    },
    
    onError: (error: Error) => {
      toast.error(error.message || 'Failed to update wine');
    },
  });
}

export function useDeleteWine() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: string) => api.deleteWine(id),
    
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['wines'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
      toast.success('Wine deleted successfully');
    },
    
    onError: (error: Error) => {
      toast.error(error.message || 'Failed to delete wine');
    },
  });
}

export function useBulkUploadWines(restaurantId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (file: File) => api.bulkUploadWines(restaurantId, file),
    
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['wines'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
      toast.success(`Successfully uploaded ${data.wines_created} wines`);
      
      if (data.errors && data.errors.length > 0) {
        toast.warning(`${data.errors.length} rows had errors`);
      }
    },
    
    onError: (error: Error) => {
      toast.error(error.message || 'Failed to upload wines');
    },
  });
}
