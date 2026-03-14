import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { RouteAuditComputeResponse, RouteAuditRecord } from '../models/route-audit.model';

export interface HealthCheckResponse {
  status: 'ok' | 'degraded';
  correlation_id?: string | null;
  database: { ok: boolean; detail: string };
  redis: { ok: boolean; detail: string };
}

@Injectable({ providedIn: 'root' })
export class ApiService {
  private readonly baseUrl = environment.apiBaseUrl;

  constructor(private readonly http: HttpClient) {}

  health(): Observable<HealthCheckResponse> {
    return this.http.get<HealthCheckResponse>(`${this.baseUrl}/health/`);
  }

  listAuditRecords(): Observable<RouteAuditRecord[]> {
    return this.http.get<RouteAuditRecord[]>(`${this.baseUrl}/audit-records/`);
  }

  createAuditRecord(payload: Omit<RouteAuditRecord, 'id' | 'created_at'>): Observable<RouteAuditRecord> {
    return this.http.post<RouteAuditRecord>(`${this.baseUrl}/audit-records/create/`, payload);
  }

  computeAudit(payload: {
    origin: string;
    destination: string;
    fleet_type: 'diesel' | 'hybrid' | 'ev';
    goal: 'fastest' | 'cheapest' | 'greenest' | 'balanced';
  }): Observable<RouteAuditComputeResponse> {
    return this.http.post<RouteAuditComputeResponse>(`${this.baseUrl}/audit/compute/`, payload);
  }
}
