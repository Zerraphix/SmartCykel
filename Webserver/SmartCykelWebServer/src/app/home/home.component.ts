import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { RouterModule } from '@angular/router';
import { ThingsboardTestService } from '../thingsboard-test.service';

interface TbPoint {
  ts: number;
  value: any;
}

@Component({
  selector: 'app-homepage',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  // UI fields used in your template
  isConnected = false;

  batteryLevel = 0;          
  batteryRemainingText = '';   
  batteryRemainingHours: number | null = null;
  batteryVoltage: number | null = null;
  batteryCurrent: number | null = null;
  batteryState = '';           
  batteryCharging = false;

  humidity: number | null = null;
  latitude: number | null = null;
  longitude: number | null = null;

  estimatedRangeKm: number | null = null;
  lastRideSummary = 'No ride data yet.';
  lastUpdate: Date | null = null;

  constructor(private tbService: ThingsboardTestService) {}

  ngOnInit(): void {
    this.refreshTelemetry();

    // optional: auto-refresh every 30 seconds
    // setInterval(() => this.refreshTelemetry(), 30000);
  }

  private getLatest(raw: any, key: string): TbPoint | null {
    const arr = raw?.[key];
    if (Array.isArray(arr) && arr.length > 0) {
      return arr[arr.length - 1];
    }
    return null;
  }

  refreshTelemetry(): void {
    this.tbService.getLatestTelemetry().subscribe({
      next: res => {
        // mark as connected if we got anything meaningful
        const socPoint = this.getLatest(res, 'battery_soc');
        this.isConnected = !!socPoint;

        // battery level
        this.batteryLevel = socPoint ? Number(socPoint.value) || 0 : 0;

        // other battery fields
        const remText = this.getLatest(res, 'battery_remaining_text');
        this.batteryRemainingText = remText ? String(remText.value) : '';

        const remH = this.getLatest(res, 'battery_remaining_hours');
        this.batteryRemainingHours = remH ? Number(remH.value) || null : null;

        const volt = this.getLatest(res, 'battery_voltage');
        this.batteryVoltage = volt ? Number(volt.value) || null : null;

        const cur = this.getLatest(res, 'battery_current');
        this.batteryCurrent = cur ? Number(cur.value) || null : null;

        const state = this.getLatest(res, 'battery_state');
        this.batteryState = state ? String(state.value) : '';

        const charging = this.getLatest(res, 'battery_charging');
        this.batteryCharging = charging ? charging.value === 'true' || charging.value === true : false;

        // humidity & location
        const hum = this.getLatest(res, 'humidity');
        this.humidity = hum ? Number(hum.value) || null : null;

        const lat = this.getLatest(res, 'latitude');
        this.latitude = lat ? Number(lat.value) || null : null;

        const lon = this.getLatest(res, 'longitude');
        this.longitude = lon ? Number(lon.value) || null : null;

        // estimated range – for now just fake: hours * 15 km/h
        if (this.batteryRemainingHours != null) {
          this.estimatedRangeKm = Math.round(this.batteryRemainingHours * 15);
        } else {
          this.estimatedRangeKm = null;
        }

        // last update time – just use the newest ts we saw
        const allPoints = [
          socPoint, remText, remH, volt, cur, hum, lat, lon
        ].filter(p => !!p) as TbPoint[];
        if (allPoints.length) {
          const maxTs = Math.max(...allPoints.map(p => p.ts));
          this.lastUpdate = new Date(maxTs);
        }

        // simple last ride placeholder using location / soc
        this.lastRideSummary = this.latitude != null && this.longitude != null
          ? `Bike last seen at (${this.latitude.toFixed(4)}, ${this.longitude.toFixed(4)}), battery ${this.batteryLevel}%.`
          : `Battery at ${this.batteryLevel}% – more ride data coming later.`;
      },
      error: err => {
        console.error('Failed to load telemetry', err);
        this.isConnected = false;
      }
    });
  }

  // existing button handlers
  onStartRide(): void {
    console.log('Start ride clicked');
  }

  onViewBikes(): void {
    console.log('View bikes clicked');
  }
}
