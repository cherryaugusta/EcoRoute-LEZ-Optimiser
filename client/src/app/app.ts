import { CommonModule } from '@angular/common';
import { Component, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ApiService, HealthCheckResponse } from './services/api';
import { RouteAuditComputeResponse } from './models/route-audit.model';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <main style="font-family: system-ui; margin: 2rem; max-width: 980px;">
      <h1>EcoRoute LEZ Optimiser</h1>
      <p><strong>Audit mode</strong>: compliance explanation + emissions breakdown (typed contract).</p>

      <section style="margin-top: 1.25rem;">
        <button type="button" (click)="checkHealth()">Check API Health</button>
        <pre *ngIf="health() as h">{{ h | json }}</pre>
      </section>

      <section style="margin-top: 1.25rem;">
        <h2>Compute audit (deterministic example)</h2>
        <div style="display: grid; gap: .5rem; grid-template-columns: 1fr 1fr;">
          <label>
            Origin
            <input [(ngModel)]="origin" />
          </label>

          <label>
            Destination
            <input [(ngModel)]="destination" />
          </label>

          <label>
            Fleet
            <select [(ngModel)]="fleet">
              <option value="diesel">diesel</option>
              <option value="hybrid">hybrid</option>
              <option value="ev">ev</option>
            </select>
          </label>

          <label>
            Goal
            <select [(ngModel)]="goal">
              <option value="fastest">fastest</option>
              <option value="cheapest">cheapest</option>
              <option value="greenest">greenest</option>
              <option value="balanced">balanced</option>
            </select>
          </label>
        </div>

        <button type="button" style="margin-top: .75rem;" (click)="compute()">Compute</button>
        <pre *ngIf="computeResp() as r">{{ r | json }}</pre>
      </section>
    </main>
  `,
})
export class App {
  health = signal<HealthCheckResponse | null>(null);
  computeResp = signal<RouteAuditComputeResponse | null>(null);

  origin = 'London Bridge';
  destination = 'Heathrow T5';
  fleet: 'diesel' | 'hybrid' | 'ev' = 'ev';
  goal: 'fastest' | 'cheapest' | 'greenest' | 'balanced' = 'greenest';

  constructor(private readonly api: ApiService) {}

  checkHealth(): void {
  this.api.health().subscribe({
    next: (v) => this.health.set(v),
    error: (e) => {
      if (e?.error) {
        this.health.set(e.error);
      } else {
        this.health.set({
          status: 'degraded',
          correlation_id: null,
          database: { ok: false, detail: 'Health check failed' },
          redis: { ok: false, detail: 'Health check failed' },
        });
      }
    },
  });
}

  compute(): void {
    this.api
      .computeAudit({
        origin: this.origin,
        destination: this.destination,
        fleet_type: this.fleet,
        goal: this.goal,
      })
      .subscribe({
        next: (v) => this.computeResp.set(v),
        error: (e) => {
          console.error('Compute failed:', e);
          this.computeResp.set(null);
        },
      });
  }
}
