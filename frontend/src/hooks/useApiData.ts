import { useState, useEffect, useCallback } from 'react';
import { apiService } from '../services/api';
import type { Project, Experience } from '../services/api';

interface UseApiDataState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
}

interface UseApiDataReturn<T> extends UseApiDataState<T> {
  refetch: () => Promise<void>;
}

// Hook for fetching projects
export function useProjects(
  featuredOnly: boolean = false
): UseApiDataReturn<Project[]> {
  const [state, setState] = useState<UseApiDataState<Project[]>>({
    data: null,
    loading: true,
    error: null,
  });

  const fetchProjects = useCallback(async () => {
    setState(prev => ({ ...prev, loading: true, error: null }));

    const response = await apiService.getProjects(featuredOnly);

    if (response.error) {
      setState({
        data: null,
        loading: false,
        error: response.error,
      });
    } else {
      setState({
        data: response.data,
        loading: false,
        error: null,
      });
    }
  }, [featuredOnly]);

  useEffect(() => {
    fetchProjects();
  }, [fetchProjects]);

  return {
    ...state,
    refetch: fetchProjects,
  };
}

// Hook for fetching experience
export function useExperience(): UseApiDataReturn<Experience[]> {
  const [state, setState] = useState<UseApiDataState<Experience[]>>({
    data: null,
    loading: true,
    error: null,
  });

  const fetchExperience = useCallback(async () => {
    setState(prev => ({ ...prev, loading: true, error: null }));

    const response = await apiService.getExperience();

    if (response.error) {
      setState({
        data: null,
        loading: false,
        error: response.error,
      });
    } else {
      setState({
        data: response.data,
        loading: false,
        error: null,
      });
    }
  }, []);

  useEffect(() => {
    fetchExperience();
  }, [fetchExperience]);

  return {
    ...state,
    refetch: fetchExperience,
  };
}

// Hook for fetching a single project
export function useProject(id: number): UseApiDataReturn<Project> {
  const [state, setState] = useState<UseApiDataState<Project>>({
    data: null,
    loading: true,
    error: null,
  });

  const fetchProject = useCallback(async () => {
    setState(prev => ({ ...prev, loading: true, error: null }));

    const response = await apiService.getProject(id);

    if (response.error) {
      setState({
        data: null,
        loading: false,
        error: response.error,
      });
    } else {
      setState({
        data: response.data,
        loading: false,
        error: null,
      });
    }
  }, [id]);

  useEffect(() => {
    if (id) {
      fetchProject();
    }
  }, [fetchProject, id]);

  return {
    ...state,
    refetch: fetchProject,
  };
}

// Hook for fetching a single experience entry
export function useExperienceEntry(id: number): UseApiDataReturn<Experience> {
  const [state, setState] = useState<UseApiDataState<Experience>>({
    data: null,
    loading: true,
    error: null,
  });

  const fetchExperienceEntry = useCallback(async () => {
    setState(prev => ({ ...prev, loading: true, error: null }));

    const response = await apiService.getExperienceEntry(id);

    if (response.error) {
      setState({
        data: null,
        loading: false,
        error: response.error,
      });
    } else {
      setState({
        data: response.data,
        loading: false,
        error: null,
      });
    }
  }, [id]);

  useEffect(() => {
    if (id) {
      fetchExperienceEntry();
    }
  }, [fetchExperienceEntry, id]);

  return {
    ...state,
    refetch: fetchExperienceEntry,
  };
}
