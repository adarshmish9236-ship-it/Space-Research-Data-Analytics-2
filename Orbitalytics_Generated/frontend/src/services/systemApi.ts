import { fetchJson } from './api';
import { HDFSOwerview, DatasetItem } from '../types';

export const systemApi = {
  getSystemStatus: () => fetchJson<any>('/system/status'),
  getHDFSOverview: () => fetchJson<HDFSOwerview>('/hdfs/overview'),
  getHDFSFiles: (zone: string = 'curated') => fetchJson<any>(`/hdfs/files?zone=${zone}`),
  getHiveTables: () => fetchJson<any>('/hive/tables'),
  executeHiveQuery: (queryId: string) => fetchJson<any>(`/hive/query?query_id=${queryId}`),
  runMapReduce: (jobName: string) => fetchJson<any>(`/mapreduce/run?job_name=${jobName}`, { method: 'POST' }),
  runSparkJob: (jobName: string) => fetchJson<any>(`/spark/run?job_name=${jobName}`, { method: 'POST' }),
  getPipelineStatus: () => fetchJson<any>('/pipeline/status'),
  triggerPipeline: (profile: string = 'medium') => fetchJson<any>(`/pipeline/run?profile=${profile}`, { method: 'POST' }),
  getDatasets: () => fetchJson<DatasetItem[]>('/datasets'),
  previewDataset: (name: string, page: number = 1, pageSize: number = 20, search?: string) => {
    const params = new URLSearchParams({ page: page.toString(), page_size: pageSize.toString() });
    if (search) params.append('search', search);
    return fetchJson<any>(`/datasets/${name}/preview?${params.toString()}`);
  },
  getDatasetQuality: (name: string) => fetchJson<any>(`/datasets/${name}/quality`)
};

