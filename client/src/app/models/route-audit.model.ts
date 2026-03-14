export type FleetType = 'diesel' | 'hybrid' | 'ev';
export type OptimisationGoal = 'fastest' | 'cheapest' | 'greenest' | 'balanced';

export interface RouteAuditRecord {
  id: string;
  created_at: string;

  origin: string;
  destination: string;

  fleet_type: FleetType;
  goal: OptimisationGoal;

  restricted_zones_avoided: string[];
  compliance_explanation: string;

  estimated_cost_pence: number;
  estimated_distance_km: string;
  estimated_duration_seconds: number;

  emissions_kg_co2e: string;
  emissions_breakdown: Record<string, number>;
}

export interface RouteAuditComputeResponse {
  origin: string;
  destination: string;

  fleet_type: FleetType;
  goal: OptimisationGoal;

  restricted_zones_avoided: string[];
  compliance_explanation: string;

  estimated_cost_pence: number;
  estimated_distance_km: string;
  estimated_duration_seconds: number;

  emissions_kg_co2e: string;
  emissions_breakdown: Record<string, number>;
}
